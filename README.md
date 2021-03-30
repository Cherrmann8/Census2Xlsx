<br/>
<p align="center">
    <a href="https://github.com/Cherrmann8/Census2Xlsx/" target="_blank">
        <img width="50%" src="https://github.com/Cherrmann8/Census2Xlsx/blob/master/src/assets/icon.svg" alt="Census2Xlsx logo">
    </a>
</p>

<br/>
<p align="center">
    <a href="https://github.com/Cherrmann8/Census2Xlsx/" target="_blank">
        <img src="https://img.shields.io/badge/<build>-<passing>-<brightgreen>" alt="build status">
    </a>
</p>
<br/>

# Census2Xlsx

Census2Xlsx is a cross-platform data collection and analysis tool for the United States Census Bureau database.

# Overview

Developed with Python 3.7, Electron 11.2.1, and React 17.0.1.

Used the following guide to set up my React-Electron development environment: https://flaviocopes.com/react-electron/.

The project has a Trello board for tracking features and development tasks. This board can be viewed at: https://trello.com/b/UD66VbiG/cen2xlsx.

This application was developed for Heartland Grant Solutions: http://www.heartlandgrants.org/.

## Terminology

Location: A geographic location described by a census geocode. Locations can represent a variety of geographic levels defined but the US census. Currently support state, county, and place geographic levels.

Report Area: A set of locations.

Indicator: A data point used to convey the state, level, or amount of something.

Table: A set of related indicators.

Section: A set of related tables.

## Features

- Create a report with custom locations and indicators
- Download report as a .xlsx file
- Download report graphs as .png files

## Roadmap

- [x] ~~Write python script with hardcoded values to generate a report~~
- [x] ~~Write python script to save report as a .xlsx file~~
- [x] ~~Write python script to cache Census geocodes and tableIDs~~
- [x] ~~Prototype UI in Tkinter~~
- [x] ~~Develop UI with electron and react~~
- [ ] Add secondary features
- [ ] Implement unit tests and logging
- [ ] Build and Distribute to Windows and OSX systems

# Quickstart

Clone the repository:

```bash
$ git clone https://github.com/Cherrmann8/Census2Xlsx.git
```
