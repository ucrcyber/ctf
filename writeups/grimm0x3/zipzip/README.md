
## ZipZip (50 Points)

> My friend sent me this zip file... He is a prankster and compressed the file a LOT of times... I don't know how to make this go quickly and I don't have the time... At least he told me the password is "pass". Can you please help? 

There is a file zipped 50 times, each time with the word pass. I can use a bash script to unzip everything.

```
#!/bin/bash
for i in $(seq -f "%02g" 50 -1 0)
        do
                unzip -P pass $i.zip
                #i=$((i-1))
        done
cat flag.txt
```