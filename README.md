<br/>
<p align="center">
    <a href="https://github.com/Cherrmann8/Census2Xlsx/" target="_blank">
        <img width="25%" height="25%" src="https://github.com/Cherrmann8/Census2Xlsx/blob/master/src/assets/icon.png" alt="Census2Xlsx logo">
    </a>
</p>

<br/>
<p align="center">
    <!-- Shhh its ok... -->
    <img src="https://img.shields.io/badge/coverage-100%25-brightgreen" alt="coverage status">
    <img src="https://img.shields.io/badge/tests-passing-brightgreen" alt="test status">
    <img src="https://img.shields.io/badge/Python-3.7-informational" alt="python version">
    <img src="https://img.shields.io/badge/Electron-11.2.1-informational" alt="electron version">
    <img src="https://img.shields.io/badge/React-17.0.1-informational" alt="react version">
</p>
<br/>

# Census2Xlsx

Census2Xlsx is a cross-platform data collection and analysis tool for the United States Census Bureau database.

# Overview

Developed with Python 3.7, Electron 11.2.1, and React 17.0.1.

Used the following guide to set up my React-Electron development environment: https://flaviocopes.com/react-electron/.

The project has a Trello board for tracking features and development tasks. This board can be viewed at: https://trello.com/b/UD66VbiG/cen2xlsx.

This application was developed for Heartland Grant Solutions: http://www.heartlandgrants.org/.

Intended to be used in junction with Tableau.

## Terminology

Census2Xlsx accepts a Report Area and a set of Tables from multiple Sections from the user to create the final xlsx file.

Location: A geographic location described by a census geocode. Locations can represent a variety of geographic levels defined but the US census. Currently support state, county, and place geographic levels.

Report Area: A set of locations.

Indicator: A data point used to convey the state, level, or amount of something.

Table: A set of related indicators.

Section: A set of related tables.

## Features

- Create a Report Area

  <img src="https://github.com/Cherrmann8/Census2Xlsx/blob/master/src/assets/pages/LocationPage.PNG" alt="Location Page">

- Select Tables to be included in the report

  <img src="https://github.com/Cherrmann8/Census2Xlsx/blob/master/src/assets/pages/IndicatorPage.PNG" alt="Indicator Page">

- Confirm your selections and enter a file name

  <img src="https://github.com/Cherrmann8/Census2Xlsx/blob/master/src/assets/pages/ConfirmationPage.PNG" alt="Indicator Page">

- Download report as a .xlsx file

  <img src="https://github.com/Cherrmann8/Census2Xlsx/blob/master/src/assets/pages/DownloadPage.PNG" alt="Indicator Page">

- Once the .xlsx file has been generated, you can use Tableau to make interactive graphs and maps

  <img src="https://github.com/Cherrmann8/Census2Xlsx/blob/master/src/assets/pages/NC_Poverty_under_5.PNG" alt="Tableau Map">

## Roadmap

- [x] ~~Write python script with hardcoded values to generate a report~~
- [x] ~~Write python script to save report as a .xlsx file~~
- [x] ~~Write python script to cache Census geocodes and tableIDs~~
- [x] ~~Prototype UI in Tkinter~~
- [x] ~~Develop UI with electron and react~~
- [x] ~~Add secondary features~~
- [x] ~~Implement unit tests and logging~~
- [x] ~~Build and Distribute to Windows and OSX systems~~

# Quickstart

Clone the repository:

```bash
$ git clone https://github.com/Cherrmann8/Census2Xlsx.git
```

Download dependencies:

```bash
$ npm install
```

Start the application:

```bash
$ npm start
```

Take note to change the IS_DEV flag in the .env file when changing between development and production.

Build the application:

```bash
$ npm run build
```

Package the application using electron-builder:

```bash
$ npm run dist
```
