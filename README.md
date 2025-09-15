# JudgmentCalcNV - Nevada Judgment Management System

A comprehensive legal case management system designed specifically for Nevada legal practitioners to streamline judgment calculations, manage case information, and reduce malpractice risks through automated interest calculations.
Tech Stack: Python, NumPy, Pandas, Matplotlib, Seaborn, Plotly.

## 🎯 Project Overview

**JudgmentCalcNV** addresses the critical challenge faced by legal professionals in Nevada when dealing with complex financial calculations in legal settings. The system automates interest rate calculations, payment tracking, and judgment management while providing visual analytics for better case understanding.

### Business Problem Solved
- **Manual Calculation Errors**: Eliminates human errors in complex interest calculations
- **Cost Reduction**: Reduces dependency on expensive CPA services for routine calculations
- **Malpractice Risk**: Minimizes legal malpractice exposure through accurate calculations
- **Time Efficiency**: Streamlines judgment management processes for legal teams

## ✨ Key Features

### Core Functionality
- **Case Management**: Create, search, update, and remove legal cases
- **Party Management**: Track plaintiffs, defendants, and associated parties
- **Interest Calculations**: Automated statutory and contractual interest calculations
- **Financial Tracking**: Comprehensive liability and payment management
- **Data Visualization**: Interactive charts showing principal vs interest distributions
- **Orphaned Entry Management**: Identify and clean unlinked database entries

### Advanced Capabilities
- **Multi-type Interest Support**: Handles both prejudgment and post-judgment interest
- **Historical Rate Integration**: Uses daily historical interest rates for precise calculations
- **Visual Analytics**: Pie charts and bar graphs for financial data representation
- **Search Functionality**: Advanced search capabilities for cases and parties
- **Data Integrity**: Built-in validation and error handling

## 🏗️ System Architecture

### Database Design
The system utilizes a MySQL database with four core tables:

#### 1. CaseDetails Table
- `caseID` (INT) - Unique case identifier
- `caseNumber` (VARCHAR) - Official case number
- `createDate` (DATETIME) - Case creation timestamp
- `updateDate` (DATETIME) - Last modification timestamp

#### 2. ClientInfo Table
- `clientID` (INT) - Unique client identifier
- `firstName` (VARCHAR(50))` - Client first name
- `lastName` (VARCHAR(50))` - Client last name
- `type` (ENUM) - 'plaintiff' or 'defendant'
- `caseID` (INT) - Foreign key to CaseDetails

#### 3. Accounting Table
- `accountingID` (INT) - Unique transaction identifier
- `caseID` (INT) - Related case foreign key
- `type` (VARCHAR(50))` - Transaction type
- `amount` (DECIMAL) - Dollar amount
- `incurredDate` (DATE) - Date liability incurred

#### 4. Interest Table
- `id` (INT) - Unique record identifier
- `date` (DATE) - Effective date
- `interest` (FLOAT) - Daily interest rate

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- MySQL Database
- Required Python packages (see Installation section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/JudgmentCalcNV.git
   cd JudgmentCalcNV
   ```

2. **Install required packages**
   ```bash
   pip install --editable .
   ```

3. **Required Dependencies**
   ```bash
   pip install mysql-connector-python
   pip install matplotlib
   pip install datetime
   ```

4. **Database Configuration**
   Update the database credentials in your configuration file:
   ```python
   sqlUser = 'your_username'
   sqlPassword = 'your_password'
   sqlHost = 'your_host'
   database = 'your_database_name'
   ```

## 📖 Usage Guide

### Main Menu Options

The system provides an intuitive menu-driven interface with the following options:

1. **Create New Case** - Establish new legal cases with party and liability information
2. **Search Case** - Retrieve case details using case numbers
3. **Update Case** - Modify existing case information
4. **Remove Case** - Delete cases and associated data
5. **Calculate Interest** - Perform automated interest calculations for liabilities
6. **Manage Parties** - Add, remove, or view parties associated with cases
7. **Search Parties** - Find parties by name across all cases
8. **Check Orphaned Entries** - Identify and manage unlinked database entries
9. **Manage Liabilities** - Add or view case-related liabilities
10. **Case Visualization** - Generate charts showing case financial distributions
11. **Quit** - Exit the system

### Example Workflow

#### Creating a New Case
```python
# Select option 1 from main menu
# Enter case number (format: 2 letters + 6-8 characters)
# Example: NV123456789
# Add party information when prompted
# Add liability details as needed
```

#### Calculating Interest
```python
# Select option 5 from main menu
# Enter case number
# Choose liability for calculation
# System automatically calculates based on:
#   - Statutory rates (Nevada legal rates)
#   - Contractual rates (custom agreement rates)
# View results with optional pie chart visualization
```

### Key Programming Concepts Implemented
- ✅ **Flow Control**: Strategic use of if/else statements and loops
- ✅ **Functions**: Modular design with specialized functions
- ✅ **Data Structures**: Lists and dictionaries for data management
- ✅ **CRUD Operations**: Complete database interaction capabilities
- ✅ **Data Computation**: Complex interest calculations and financial analysis
- ✅ **Visualization**: Charts and graphs for data representation

## 📊 Data Visualization Examples

The system generates several types of visual representations:
- **Pie Charts**: Principal amount vs. total interest distribution
- **Bar Charts**: Number of parties vs. number of liabilities per case
- **Financial Summaries**: Visual breakdown of judgment components

## 🔒 Database Connection

The system connects to a secure MySQL database hosted on AWS RDS:
- **Host**: database-1.ctnfprzjtuyt.us-east-1.rds.amazonaws.com
- **Database**: DataWarehouse
- **Security**: Encrypted connections with proper authentication

### Development Guidelines
1. Follow existing code structure and naming conventions
2. Include comprehensive error handling
3. Document all new functions with appropriate docstrings
4. Test database operations thoroughly before committing
5. Maintain security best practices for database connections



