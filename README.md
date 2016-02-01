# Funnel

### About
Collects conversations from different social media and funnels them into Telegram chats.

Currently is in really early alpha: supports collection only from vk.com and has no user-facing features.

### Deployment
 - Create Telegram bot and put its key in Settings.py
 - Create vk application and authorize it to access your messages
 - Put vk token into Settings.py
 - Fill `id_converter` in DB.py with IDs of conversations needed to be linked

### Structure of application
[Diagram of the system](https://docs.google.com/drawings/d/1NiwHOa0rWSJaT0ZZxkrldaXMVUsPHpnPuBXrBtgFiaU/edit?usp=sharing) on Google Docs

`VK.receiver` – responsible for getting updates from the social network and putting them into queue.   
`VK2Telegram.converter` – takes messages from the queue, selects messages worth passing forward, transforms them to Telegram request format and puts them into another queue.  
`Telegram.sender` – takes messages from the queue and makes request.   

Every method runs in its own thread and communicates via queues.

