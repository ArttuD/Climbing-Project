<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#Plan">Plan</a>
    </li>
    <li>
        <a href="#Schematics and function">Schematics and function</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

This project aims to develop a skeleton tracking algorithm for climbers. The project utilizes 4 gyroscopes and magentometers atteched on the limbs of the object. We use python and C++. Later, we might develop a computer vision based tracking algorythm to supply data produced by the sensor fusion

Here's why:
* Fun
* Learn

<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!-- GETTING STARTED -->
## Plan

- [] Data transmission between gyros using struct and seriel print to computer
    - [ ] ID, Acc_x->z and rot_x->z
    - [ ] Serial print start "e" stop "s", and split by ","
- [] Delun Boxes for the circuit and wrist band
- [ ] Order circuits when tested
- [ ] Arttu: PID Control
    - [ ] unscented kalman filter
    - [ ] IMM filter fusion
    - [ ] sensor fusion
- [ ] Improve current video tracker 
    - [ ] calibration
    - [ ] tophat etc tricks and tips
    - [ ] ML detection to get bounding boxes


<p align="right">(<a href="#readme-top">back to top</a>)</p>
<!-- GETTING STARTED -->
## Schematics and Function


<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Clone the git and download packages provided in utilities.txt

1. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
2. Install NPM packages
   ```sh
   npm install utilities.txt -g
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

Liirum laarum

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES  Examples-->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members