# AP Research Audio Form

Recreating the form that was used in [this](https://aes.org/publications/elibrary-page/?id=16480) study from AES

Created with the closest behaviour to the form as possible, only filling the blanks when needing to.

## Behaviour

The UI pools the audio that it needs to use from the instance1.json file udner res, (will be soon expanded to different instances for a more diverse range of music)

there two trials (or songs) that the listener will rate, each trial has two steps:
* **Coarse Personalization Test**: Four versions of the songs modified with EQ curves that hold a dynamic range of 9db will be presented, and the listener will rate them based off of a ITU-R BS 1284 scale.
* **Fine Personalization Test**: The highest rated EQ curve gets determined, and listener is shown that, and another curve with a dynamic range of 4.5db

This occurs twice, and then data is dumped under the data folder as res.json

## Photos

*Trial One Coarse Personalization*
![Course Personalization](./res/readme/CP.png)

*Trial Two Fine Personalization*
![Fine Personalization](./res//readme/FP.png)

this repeats and then the data is dumped to be used later :)