# Historic Code
Things that worked but I've since removed

## Stock regex and response
```py
stonks = re.findall(r"\$[a-z][a-z][a-z]", mc)
if stonks != None and message.author.id != self.bot.user.id:
    for stonk in stonks:
        if stonk == "gme" or stonk == "amc" or stonk == "nok":
            await mchan.send("🚀 " + stonk.upper() + " TO THE MOON! 🚀")
```