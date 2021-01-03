## Hall of Fame - 22 Solves

> We made a Slack bot (@hof) to remember our past winners. Hope no one hacks it cuz we are running it on a really important database. 

On the Slack server for the challenge, we are given access to a bot. When typing the help command to see what we have access to, this is what we see:

![helpcommand](https://i.imgur.com/TDjDHY9.png)

The only command that takes in userinput is ``rank``, so that's what we will be exploiting. It takes in a team_name as the parameter. Looking at the given database file, we can see some examples of team names as well as where the flag is located ( ``Flag`` in ``Flags`` at index ``1``.)

Looking at the source code, we can see the method that queries the database with our userinput.

```
// rank <team_name>
func rankHandler(_ slacker.BotContext, request slacker.Request, response slacker.ResponseWriter) {
	teamName := request.Param("team_name")
	var r Rankings
	// query database
	_, _ = db.
		Where(fmt.Sprintf("team_name = '%s'", teamName)).
		Get(&r)
	// send response
	response.Reply(fmt.Sprintf("%d - %s", r.Rank, r.TeamName))
}
```

Let's try inputting one of the team names, ``UMR``.

```
Nathan Melwani  11:17 PM
rank UMR
hof2APP  11:17 PM
18 - UMR
```

Based on the method, we input a string and get a rank and team name out of it. This limits what information we are able to access significantly. We can assume our query is something like this:

```
SELECT * FROM rankings WHERE team_name = `<user input>`
```

We also know that we can get the flag with this query:

```
SELECT flag FROM flags
```

With this, we can create the following injection:

```
rank ' OR rank = (SELECT unicode(substr(flag,1))-105 FROM flags) OR rank = '
```

Let's go through each and every part of query. The first word `rank` is used to run the command that takes in our user input. The ``'`` character is used to close the string used for user input. We are using OR so that we can compare and get data to the flag itself. Skipping to the end, the last ``OR rank = '`` is used to close the query, so that it is valid. The full query would look something like this:

```
SELECT * FROM rankings WHERE team_name = '' OR rank = (SELECT unicode(substr(flag,1))-105 FROM flags) OR rank = ''
```

Now to explain the middle part. We will select the first character of the flag and run it through ``unicode()``, which returns an ascii value of that character of the string. The problem is, in order for the query to successfully result in output, it needs to be able to display a team name that corresponds to a proper team number. This means that the resulting number needs to be between 1 and 20, as these are the only team numbers in the database. Therefore, for the first character (and to show this injection works), I subtract it by 105. The flag format is ``we{*}``, so the first character is ``w``. We know the ascii value of ``w`` is 119. 119-105=14, so if this query works it will show the 14th ranked team.

```
Nathan Melwani  11:26 PM
rank ' OR rank = (SELECT unicode(substr(flag,1))-105 FROM flags) OR rank = '
hof2APP  11:26 PM
14 - w01verines
```

It worked! From this, you can tell that finding the full flag is very, very tedious. You have to keep guessing numbers to subtract by until you find one that is 20 lower than the correct char at that position. Here is one more example. The third char is ``{`` as per the flag format. The ascii value of ``{`` is 123. Therefore, we can use the following injection:

```
Nathan Melwani  11:39 PM
rank ' OR rank = (SELECT unicode(substr(flag,3))-120 FROM flags) OR rank = '
hof2APP  11:39 PM
3 - lsof -i:80
```

Sure enough, 123 (the unicode value at position 3) - 120 = 3, and we are able to see that it is 3 from the slack bot's output. If we were to subtract by a different number, say 60, then 123-60 > 20, so we will not see any output, as there is no corresponding team name for number 63. 

This means you will have to guess what to subtract by, as the range for values in the flag vary greatly. The values that make up the flag, ``-, 0-9, a-z, {, }`` span over 80 numbers, so finding the flag is very time consuming.

Here is the final flag:

```
we{676d13f9-47ef-4364-bc40-09d7761f9a58-br3k-s1ack-8y-sq1-inject1on}
```