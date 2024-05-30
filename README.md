# PIXELPULSE

* [X] to find out which window the user is on

  `used pygetwindows for getting what is the active windows of the user  , also gets which file and what directory is the user working on and on which tab in which browser is the user currently `
* [ ] find out the time the user is on that window

  `set a timer which runs until the tabs are switched `
* [ ] save it in a json format or a csv format

  `to save an activity in a json format with the time spent on it , also if an user has used brave , the activity title is in the format ```Should I make variables private in my class? : r/learnpython - Brave ``` . so need to introduce child nodes inside the dictionary , like brave has a child node with the name r/learnpython which has a child node named the title of that reddit post , it should also have its own time spent section , which gets added to the parent node , so like i spent 10 min on a post on r/learnpython and 20 mins on other post of r/learnpython , so in the time section of parent node which is r/learnpython , it should show a cumulation of 10+20=30 minutes `
* [ ] save that data in a server
* [ ] deploy a flask app
* [ ] User authentication
* [ ] gets data from the server
* [ ] shows analytics of that particular user
* [ ] make a interactive tree which shows what were the footprints of an user at a particular time

  `like at 3:30 i was surfing r/learnpython , so i should be able to set a time stamp at a particular time and the graph should be minimised into a tree which shows my tracks at 3:30 about what was i surfing at that time and through which paths i got there `

#### CHALLENGES

the spotify when at home page shows `spotify premium` but when i go to a particular album it doesnt shows if the spotify is playing or not , it just shows like this `Playboi Carti - Control`
