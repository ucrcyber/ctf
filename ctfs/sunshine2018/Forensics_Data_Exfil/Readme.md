So we have a standard .pcap challenge, boot up wireshark

Everything is really standard, just TCP connections and regular HTTP connections that are empty. 

There are no outgoing HTTP requests or anything else that would indicate a standard download, so lets check our .log files

We can identify a few IPs, just going through them we can see one particularly suspicious IP (that isn't mail.ru)

Name: 504b030414000000000030be774c973a10791e0000001e0000000a000000.cozybear.group

This obviously is not normal, as the responses are 127.0.0.1, the loopback address, and there are multiple of these in a row

Upon further inspection, this is likely hexadecimal, and 50 4b 03 04 represents the file header for compressed files like .zip

So, put it together, open up a hex editor, and we're done