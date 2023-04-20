<div align="center">
  <a href="#">
  </a>
  <h3 align="center">wAIfuS</h3>
  <p align="center">
    AI Chatbot with Conversation Memory and Stored Knowledge Base
    <br />
    <a href="https://github.com/SynthpX/wAIfuS/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="hhttps://github.com/SynthpX/wAIfuS/">View Demo</a>
    ·
    <a href="https://github.com/SynthpX/wAIfuS/issues">Report Bug</a>
    ·
    <a href="https://github.com/SynthpX/wAIfuS/issues">Request Feature</a>
  </p>
</div>

## Built With

1. OpenAI
2. Voicevox API
3. Silero TTS 
4. [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
5. [Text Classification](https://huggingface.co/j-hartmann/emotion-english-distilroberta-base) (Used on Emotion Recognition)
6. [REMO](https://github.com/daveshap/REMO_Framework)


## About The Project
This advanced AI chatbot is designed to retain past conversations and leverage a knowledge base stored in SQLite. 
The current iteration is under heavy development and not intended for public use, it offers a glimpse of the powerful features being integrated (that is why it dosent have req.txt).


## Features

- [x] Add Stored Knowledge Base
- [ ] Expanding and refining the knowledge base
    - [ ] Customized AI Identity
    - [ ] Implement Conversation Summary Memory
- [x] Emotion recognition (Implemented but Intended for Vtube Audio)
- [x] Enhancing TTS capabilities and exploring custom TTS options
    - [ ] Train/Use Custom Model for TTS
- [x] Multi-language Support (adding more LANG is always an option)
    - [x] Indonesia
    - [x] English
    - [x] Japanese
- [x] Translator Support (adding more translator is always an option, im also considering using [OpenAI as translator](https://arxiv.org/pdf/2301.08745v2.pdf))
    - [x] DeepLx
    - [x] DeepL (Need Pro)
    - [x] Google Translate

# Known Issue

- [ ] 15.04.23 It took quite a long time after the app is closed due to request to OPENAI to create Knowledge Base.
- [ ] 15.04.23 If the app crash during conversation the Knowledge wont be saved.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

Suggestions are welcomed!
See the [open issues](https://github.com/SynthpX/wAIfuS/issues) for a full list of proposed features (and known issues).
This project is inspired by the works of ardha27 and sociallyineptweeb

<p align="right">(<a href="#readme-top">back to top</a>)</p>