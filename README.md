<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# EXPENSE TRACKER 🎯

## Basic Details

### Team Name: Techies

### Team Members
- Member 1: [Anamika Lily] - [AISAT]
- Member 2: [Samvritha V.S] - [AISAT]

### Hosted Project Link
http://127.0.0.1:5000

### Project Description
An Expense Tracker with Budget Planner is a web application that helps users record their daily expenses and manage their income effectively. It allows users to set monthly budgets, track spending by category, and monitor savings. This helps user to control unnecessary expenses and improve financial planning habits.

### The Problem statement
An Expense Tracker with Budget Planner solves the problem of unorganized spending and poor financial planning faced by many individuals. People often lose track of daily expenses and exceed their budgets without realizing it. This system helps users monitor their income and expenses, control overspending, and manage savings more effectively.

### The Solution
We are solving this by creating a web-based Expense Tracker with Budget Planner that records daily income and expenses and automatically updates the remaining balance in the database. The system securely stores user data even after logout and provides real-time budget tracking and spending analysis. This helps users manage their money efficiently and avoid overspending.

---

## Technical Details

### Technologies/Components Used

**For Software:**
- Languages used: HTML, Javascript, CSS
- Frameworks used: Flask, HTML, SQLite
- Libraries used: Flask, Chart.js
- Tools used: VS Code, SQLite, Git & GitHub, Vercel, Chrome Browser

**For Hardware:**
- Main components: Laptop, Internet Connection, Cloud Server
- Specifications: Processor: Intel i3 / i5 or higher, RAM: Minimum 4GB (8GB recommended), Storage: 256GB HDD/SSD, Operating System: Windows 10/11 / macOS / Linux
- Tools required: VS Code (Code Editor), Python (Flask Framework), SQLite Database, Git & GitHub, Chrome Browser (Testing), Vercel (Deployment)

## Features

List the key features of your project:
- Feature 1: User Authentication System
  Secure login and registration with password hashing and OTP-based password reset to protect user accounts.
- Feature 2:  Monthly Budget Planning
  Users can set a monthly budget and track how much amount is used and remaining in real time.
- Feature 3: Category-Based Expense Tracking
  Users can create categories (Cash, GPay, Bank, etc.) and record income and expenses separately for better management.
- Feature 4: Data Persistence & Reports
  All transactions are stored in the database and displayed with summary cards and charts for easy analysis.


## Implementation

### For Software:

#### Installation
```bash
Installation commands - pip install -r requirements.txt
```

#### Run
```bash
Run commands - python app.py
http://127.0.0.1:5000
```

### For Hardware:

#### Components Required
[List all components needed with specifications]

#### Circuit Setup
[Explain how to set up the circuit]

---

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

https://drive.google.com/drive/folders/1BzuyPMPLJ5_A2ySMu7LXYnGZLnOpLhEi?usp=drive_link
It includes 8 screenshots and 1 video of the working project in it.

#### Diagrams

**System Architecture:**

![Architecture Diagram](docs/architecture.png)
https://drive.google.com/drive/folders/1neF46znQvtgWNDy4cOugUWLVoYe3UaOY?usp=drive_link
It is a basic flowchart to easily understand

---

### For Hardware:

#### Schematic & Circuit

![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

#### Build Photos

![Team](Add photo of your team here)

![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

---

## Additional Documentation

### For Web Projects with Backend:

#### API Documentation

**Base URL:** `https://api.yourproject.com`

##### Endpoints

**GET /api/endpoint**
- **Description:** [What it does]
- **Parameters:**
  - `param1` (string): [Description]
  - `param2` (integer): [Description]
- **Response:**
```json
{
  "status": "success",
  "data": {}
}
```

**POST /api/endpoint**
- **Description:** [What it does]
- **Request Body:**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```
- **Response:**
```json
{
  "status": "success",
  "message": "Operation completed"
}
```

[Add more endpoints as needed...]

---

### For Mobile Apps:

#### App Flow Diagram

![App Flow](docs/app-flow.png)
*Explain the user flow through your application*

#### Installation Guide

**For Android (APK):**
1. Download the APK from [Release Link]
2. Enable "Install from Unknown Sources" in your device settings:
   - Go to Settings > Security
   - Enable "Unknown Sources"
3. Open the downloaded APK file
4. Follow the installation prompts
5. Open the app and enjoy!

**For iOS (IPA) - TestFlight:**
1. Download TestFlight from the App Store
2. Open this TestFlight link: [Your TestFlight Link]
3. Click "Install" or "Accept"
4. Wait for the app to install
5. Open the app from your home screen

**Building from Source:**
```bash
# For Android
flutter build apk
# or
./gradlew assembleDebug

# For iOS
flutter build ios
# or
xcodebuild -workspace App.xcworkspace -scheme App -configuration Debug
```

---

### For Hardware Projects:

#### Bill of Materials (BOM)

| Component | Quantity | Specifications | Price | Link/Source |
|-----------|----------|----------------|-------|-------------|
| Arduino Uno | 1 | ATmega328P, 16MHz | ₹450 | [Link] |
| LED | 5 | Red, 5mm, 20mA | ₹5 each | [Link] |
| Resistor | 5 | 220Ω, 1/4W | ₹1 each | [Link] |
| Breadboard | 1 | 830 points | ₹100 | [Link] |
| Jumper Wires | 20 | Male-to-Male | ₹50 | [Link] |
| [Add more...] | | | | |

**Total Estimated Cost:** ₹[Amount]

#### Assembly Instructions

**Step 1: Prepare Components**
1. Gather all components listed in the BOM
2. Check component specifications
3. Prepare your workspace
![Step 1](images/assembly-step1.jpg)
*Caption: All components laid out*

**Step 2: Build the Power Supply**
1. Connect the power rails on the breadboard
2. Connect Arduino 5V to breadboard positive rail
3. Connect Arduino GND to breadboard negative rail
![Step 2](images/assembly-step2.jpg)
*Caption: Power connections completed*

**Step 3: Add Components**
1. Place LEDs on breadboard
2. Connect resistors in series with LEDs
3. Connect LED cathodes to GND
4. Connect LED anodes to Arduino digital pins (2-6)
![Step 3](images/assembly-step3.jpg)
*Caption: LED circuit assembled*

**Step 4: [Continue for all steps...]**

**Final Assembly:**
![Final Build](images/final-build.jpg)
*Caption: Completed project ready for testing*

---

### For Scripts/CLI Tools:

#### Command Reference

**Basic Usage:**
```bash
python script.py [options] [arguments]
```

**Available Commands:**
- `command1 [args]` - Description of what command1 does
- `command2 [args]` - Description of what command2 does
- `command3 [args]` - Description of what command3 does

**Options:**
- `-h, --help` - Show help message and exit
- `-v, --verbose` - Enable verbose output
- `-o, --output FILE` - Specify output file path
- `-c, --config FILE` - Specify configuration file
- `--version` - Show version information

**Examples:**

```bash
# Example 1: Basic usage
python script.py input.txt

# Example 2: With verbose output
python script.py -v input.txt

# Example 3: Specify output file
python script.py -o output.txt input.txt

# Example 4: Using configuration
python script.py -c config.json --verbose input.txt
```

#### Demo Output

**Example 1: Basic Processing**

**Input:**
```
This is a sample input file
with multiple lines of text
for demonstration purposes
```

**Command:**
```bash
python script.py sample.txt
```

**Output:**
```
Processing: sample.txt
Lines processed: 3
Characters counted: 86
Status: Success
Output saved to: output.txt
```

**Example 2: Advanced Usage**

**Input:**
```json
{
  "name": "test",
  "value": 123
}
```

**Command:**
```bash
python script.py -v --format json data.json
```

**Output:**
```
[VERBOSE] Loading configuration...
[VERBOSE] Parsing JSON input...
[VERBOSE] Processing data...
{
  "status": "success",
  "processed": true,
  "result": {
    "name": "test",
    "value": 123,
    "timestamp": "2024-02-07T10:30:00"
  }
}
[VERBOSE] Operation completed in 0.23s
```

---

## Project Demo

### Video
https://drive.google.com/file/d/1XKepiTFBguSVxdidFL5CPtaHzSUl0AZX/view?usp=drive_link


### Additional Demos
[Add any extra demo materials/links - Live site, APK download, online demo, etc.]

---

## AI Tools Used (Optional - For Transparency Bonus)

If you used AI tools during development, document them here for transparency:

**Tool Used:**  Frontend: HTML, CSS, Bootstrap
                Backend: Python (Flask)
                Database: MySQL
                API Testing: Postman
                Version Control: GitHub
                Deployment/Storage: Google Drive (for files if used)

**Purpose:** [What you used it for]
      To develop a user-friendly web application
      To store and manage data efficiently
      To provide secure login and data storage
      To make the system accessible and easy to use

**Key Prompts Used:**
Build a full-stack responsive web application called Smart Student Expense & Budget Planner that functions as a modern dashboard-style website and behaves like an installable Chrome application. The system must include secure user authentication where users can register and log in using email and password, with passwords securely hashed before storing in a relational database. After successful login, create a session so the user remains authenticated and the login page must not appear again unless the user explicitly logs out. A logout button must be placed at the top-left corner of the dashboard, and clicking it should properly destroy the session and redirect the user to the login page. Unauthorized users must not be able to access the dashboard without logging in.

After login, the user should be redirected to a clean, responsive dashboard interface that works smoothly on both desktop and mobile devices. At the top of the dashboard, include a month and year dropdown filter so that when the user selects a specific month, all displayed financial data dynamically updates to show only the data related to that selected month. The dashboard must display summary cards showing Total Monthly Budget, Total Expense, Remaining Balance, and Expense Usage Percentage. If total expenses reach or exceed 80% of the monthly budget, display a yellow warning message, and if expenses exceed 100%, display a red alert message. The monthly budget feature must be optional, allowing users to add or edit the budget for each month but not forcing them to set one.

Below the summary section, provide category management functionality where users can create, edit, and delete categories representing payment sources such as Cash, GPay, SBI Bank, HDFC Bank, or any custom name. Each category must store a category name, an opening balance for the selected month, and an automatically calculated remaining balance. Inside each category, users must be able to add transactions with fields including date, description or reason, type (income or expense toggle), and amount. Each transaction must be editable and deletable. When a transaction is added, the system must automatically update the category’s remaining balance (increase for income, decrease for expense), update total monthly expense, recalculate remaining balance, and refresh the expense usage percentage in real time.

At the bottom of the dashboard, include a dynamic chart (such as a pie or bar chart using Chart.js) that displays category-wise expense breakdown like travel, food, study, shopping, and others, and ensure the chart updates automatically when the month filter changes. All data including users, categories, transactions, and budgets must be permanently stored in the database so that logging out does not delete any saved information. When the user logs in again, the system must retrieve and display previously saved data correctly. Structure the database with tables for Users (id, email, password), Categories (id, user_id, name, opening_balance, month), Transactions (id, user_id, category_id, type, amount, reason, date), and Budgets (id, user_id, month, monthly_budget). Ensure clean UI/UX with a dashboard layout, card-based summaries, smooth navigation, proper session handling, input validation, secure authentication, dynamic calculations, and a professional finance-app appearance that can later be extended into a Progressive Web App.

**Percentage of AI-generated code:** [Approximately X%]

**Human Contributions:**
- Architecture design and planning
- Custom business logic implementation
- Integration and testing
- UI/UX design decisions

*Note: Proper documentation of AI usage demonstrates transparency and earns bonus points in evaluation!*

---

## Team Contributions

- [Anamika Lilly]: Designed frontend pages
                   Developed backend logic
                   Integrated database
                   Tested APIs using Postman
                   Debugging and final integration
- [Samvritha V.S]: Assisted in UI design
                   Helped in database design
                   Conducted testing
                   Documentation and PPT preparation

---

## License

This project is licensed under the [LICENSE_NAME] License - see the [LICENSE](LICENSE) file for details.

**Common License Options:**
- MIT License (Permissive, widely used)
- Apache 2.0 (Permissive with patent grant)
- GPL v3 (Copyleft, requires derivative works to be open source)

---

Made with ❤️ at TinkerHub
