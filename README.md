# Lunchbell

**One-line summary:**  
Lunchbell is a full-stack web application designed to streamline the delivery of nutritious mid-day meals by connecting rural schools, local farmers, and community surplus food donors in India.

---

## Table of Contents
- [Problem Statement](#problem-statement)  
- [Solution](#solution)  
- [Features](#features)  
- [Architecture & Technologies](#architecture--technologies)  
- [Demo](#demo)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Usage](#usage)  
- [Use Case & Impact](#use-case--impact)  
- [Challenges & Learnings](#challenges--learnings)  
- [Future Work](#future-work)  
- [Credits & Acknowledgements](#credits--acknowledgements)  
- [License](#license)  

---

## Problem Statement
In India’s remote and under-funded schools, the mid-day meal scheme often faces logistical and quality challenges—leading to food scarcity, waste, or even tragic outcomes.  
Farmers with surplus produce in rural regions struggle to access stable demand, and community surplus food often goes unused.  
There is a need for a platform that **efficiently connects** local supply (farmers, households) with demand (schools), ensuring **affordable**, **safe**, and **nutritious** meals.

---

## Solution
Lunchbell builds a trusted marketplace and management system that:  
- Enables small-scale farmers to list fresh produce surplus and sell directly to rural schools at fair rates.  
- Supports households or community members to donate healthy excess food for school meals.  
- Allows school meal administrators to forecast required quantities of ingredients, plan menus, and order accordingly.  
- Presents a web-based interface (front end) and backend database to **track**, **manage**, and **report** meal logistics end-to-end.

---

## Features
- Marketplace listings for farmers → schools, and donors → schools  
- Ingredient quantity calculator for meal planning  
- User registration & login for farmers, donors, and schools  
- Listing pages, purchase or donation flow  
- Simple UI built with HTML/CSS/JavaScript + Jinja2 templating  
- Backend powered by Python (Flask) + MySQL database  
- Dashboard/history pages for tracking past orders/donations  

---

## Architecture & Technologies
**Technologies used:**  
- Python (Flask) for server-side logic  
- HTML5 / CSS3 for structure and styling  
- JavaScript for interactive frontend behavior  
- Jinja2 templating for dynamic server-rendered pages  
- MySQL database for storing users, listings, orders, and donations  

**High-level workflow:**  
1. User (farmer/donor/school) registers and logs in  
2. Farmer/donor lists produce or food item  
3. School views available listings, calculates needed quantity, and places order or accepts donation  
4. Order/donation data stored, history tracked, notifications/confirmations issued  

---

## Demo
Watch this short walkthrough video:  
[![Lunchbell Demo](https://img.youtube.com/vi/oWbgjHm7XDY/0.jpg)](https://youtu.be/oWbgjHm7XDY)  

---

## Getting Started

### Prerequisites
- Python 3.x  
- MySQL server running or equivalent relational DB  
- (Optional) Virtual environment recommended  

### Installation
```bash
git clone https://github.com/nikanair/Lunchbell.git
cd Lunchbell
pip install -r requirements.txt
# Set up MySQL database with appropriate tables (see sql/schema.sql if available)
