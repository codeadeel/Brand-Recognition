# Brand Recognition
![DockerHub CI][dockerBadge]

![Brand Recognition Macro Architecture][macro_architecture]

The subject repository is responsible for Brand Recognition. Final classification is implemented as server-client architecture. Scenes under consideration are segregated using features extraction and matching using deep learning tools. This system can be applied on multiple streams for identification of different scenes, already available in feature store. Simply explained, if a scene to be tracked is available, it can be identified on live stream.

The model used in this architecture is ***ResNet-18***, on ***Pytorch*** framework.

##### For extensive documentation, please check [***wiki***](https://github.com/codeadeel/Brand-Recognition/wiki).

[dockerBadge]: https://github.com/codeadeel/Brand-Recognition/actions/workflows/dockerPush.yml/badge.svg?event=push
[macro_architecture]: ./MarkDown-Data/macro_architecture.jpg
