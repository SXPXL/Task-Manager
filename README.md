#  Project-X

**Tagline**: A group project management web-based app.



##  Description

Project-X is a full-stack web application designed to simplify group project and task management. It offers user registration, authentication, role-based access control, and dashboards that help users manage and track their assigned tasks. Admins and managers can create and assign tasks, while members can update progress and collaborate through comments and emails.



##  Features

- User Registration and Login  
- JWT-based Authentication  
- Role-Based Access Control 
- Create and Manage Projects  
- Create, Assign, and Track Tasks  
- Add Comments and Emails to Tasks  
- User Summary Dashboard  



##  Tech Stack

- **Frontend**: React  
- **Backend**: FastAPI
- **Authentication**: JWT(OAuth2 via FastAPI)
- **Database**: SQLite


## Prerequisites
 - Python 3.7 or higher
 - Node v16 or higher

## Installation & Setup

### Backend

1. **Clone the repository**:  
Open terminal and paste the code below
```bash
git clone https://github.com/SXPXL/Task-Manager.git
```
2. **Create a virtual environment**:  
  In your teminal, paste the code to go to the Backend folder
```bash
cd Task-Manager/Backend
```
  Paste the code in your terminal to create a virtual environment
```bash
python -m venv venv
```
  Activate the virtual environment
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. **Install the requirements**:  
   Paste the code below in the terminal to install the required packages to run the backend
```bash   
pip install -r requirements.txt
```
4. **Run the app**:  
**Note**: Ensure no other service is running on `http://localhost:8000` before starting the backend.  
Paste this code to start the backend server
```bash   
uvicorn main:app --reload
```

### Frontend
1. **Installing required packages**:  
Open a new terminal and paste the code.
```bash
cd frontend
```
Paste this code to install all the necessary packages
```bash
npm install
```
2. **Start the server**:  
Paste this code in terminal and wait for the server to start
```bash
npm start
```

`Note`: Make sure the backend is running before launching the frontend.  
Now open your Browser and go to `http://localhost:3000/` to test the app

---

##  Usage

- Users can register with a new account but are assigned the `member` role by default.
- **Admins** have full control: they can manage users, create projects and tasks, and assign roles.
- **Managers** can create and assign projects and tasks.
- **Members** can:
  - View and update tasks assigned to them
  - Add comments/emails
  - View their dashboard stats

###  Admin Demo Credentials

```
email: admin@gmail.com
Password: Admin123*
```


## Role-based Permissions

| Role    | Permissions                                                                 |
|---------|------------------------------------------------------------------------------|
| Admin   | Full system access: user management, projects, tasks                        |
| Manager | Can create/edit/delete projects and tasks                                    |
| Member  | Can view assigned projects/tasks, update tasks, and add comments/emails     |


##  Contributions

Contributions are welcome!  
To contribute:

1. Fork the repository  
2. Create a new branch (`git checkout -b feature-name`)  
3. Make your changes and **document your code properly**
4. Test your code and make sure everything works well
5. Commit the changes to your branch
6. Submit a pull request explaining your changes

Please ensure your code is clean, well-documented, and understandable before submitting a PR.

## Endpoints

### User Management
- `POST /register`: Registers a new user
- `POST /login`: Allows user to login
- `GET /get-users`: To fetch the list of all users
- `PUT /change-role/{user-id}?role=`: To change the role of a user
- `DELETE /users/{user_id}`: Deletes a user

### Project Management
- `POST /create-projects`: Creates a new project
- `GET /get-projects`: To fetch the list of all projects
- `DELETE /delete-project/{project_id}`: To delete a project

### Task CRUD
- `POST /create-tasks`: Creates a new task
- `GET /{project_id}/tasks`: To fetch all the tasks under a project
- `PUT /update-task/{task_id}`: To update a task
- `DELETE /delte-task/{task_id}`: To delete a task

 ### Attachments
 - `POST /tasks/{task_id}/attachments`: To upload an email
 - `GET /tasks/{task_id}/attachments/`: To fetch all the emails under a task
 - `GET /attachments/download/{attachment_id}`: To download an email

### Comments CRUD
- `POST /task/{task_id}`: Creates a comment
- `GET /task/{task_id}`: To fetch all comments under a task
- `PUT /comments/{comment_id}`: To update a comment
- `DELETE /{comment_id}`: Deletes a comment

### Summary
- `GET /user-summary`: To fetch the task summary of a user
- `GET /project-summary`: To fetch the summary of a project
- `GET /tasks/{status}`: Fetches summary based on certain filters

## Detailed Enpoint Information

### User Management
#### Register
**Endpoint**: POST /register  
**Description**: Allows a new user to create an account in the app  

**Request**
```json
{
  "username": "New",
  "email": "new@example.com",
  "password": "String123*"
}
```
**Response**
```json
{
    "id": 3,
    "username": "New",
    "email": "new@example.com",
    "role": "member"
}
```
#### Login
**Endpoint**: POST /login  
**Description**: Allow user login  

**Request**
```json
{
  "email": "new@example.com",
  "password": "String123*"
}
```
**Response**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6Ik5ldyIsImVtYWlsIjoibmV3QGV4YW1wbGUuY29tIiwicm9sZSI6Im1lbWJlciIsImV4cCI6MTc0ODQyNDY5MX0.ZRdx7YgEdcN0ukwQCiHDEanQ6B6rdTlapzhXkZebhZI",
    "token_type": "bearer"
}
```

#### Fetch Users
**Endpoint**: POST /get-users  
**Description**: Fetches all users in the database  

**Response**
```json
[
  {
    "id": 3,
    "username": "New",
    "email": "new@example.com",
    "role": "member"
  }
]
```

#### Role Updation
**Endpoint**: PUT /change-role/{user-id}?role=role  
**Description**: Allows to change the role of a user  

- Parameters
  - user_id = 3 (path)
  - role = manager (query)

**Response**
```json
{
  "username": "New",
  "id": 3,
  "hashed_password": "$2b$12$CHA04p8/vxP3MgsvrEHHfu1E6biMfJtSZaFWl.Arsa.L4Yb3nD/ou",
  "email": "new@example.com",
  "role": "manager"
}
```
#### Delete User
**Endpoint**: DELETE /users/{user_id}  
**Description**: To delete a user  

- Parameters
  -user_id = 3 (path)

**Response**
```json
{
    "message": "User 'New' deleted successfully"
}
```
### Project Management

#### Create Project
**Endpoint**: POST /create-projects  
**Description**: Creates a new project

**Request**
```json
{
  "title": "New project",
  "description": "This is a test"
}
```

**Response**
```json
{
  "title": "New project",
  "id": 4,
  "description": "This is a test"
}
```

#### Get Projects
**Endpoint**: GET /get-projects  
**Description**: Retrieves all projects

**Response**
```json
[
  {
    "id": 4,
    "title": "New project",
    "description": "This is a test"
  }
]
```

#### Delete Project
**Endpoint**: DELETE /delete-project/{project_id}  
**Description**: Deletes a project by ID

- Parameters
  - project_id = 4 (path)

**Response**
```json
{
  "message": "Project has been deleted successfully"
}
```

### Task CRUD

#### Create Task
**Endpoint**: POST /create-tasks  
**Description**: Creates a new task

**Request**
```json
{
  "title": "Task 1",
  "description": "Task description",
  "due_date": "2025-05-28",
  "start_date": "2025-05-28",
  "assigned_to": 1,
  "project_id": 3
}
```

**Response**
```json
{
  "id": 5,
  "title": "Task 1",
  "status": "pending",
  "start_date": "2025-05-28",
  "project_id": 3,
  "description": "Task description",
  "due_date": "2025-05-28",
  "assigned_to": 1
}
```

#### Get Tasks by Project
**Endpoint**: GET /{project_id}/tasks  
**Description**: Retrieves tasks for a specific project

- Parameters
  - project_id = 3 (path)

**Response**
```json
[
  {
    "id": 5,
    "title": "Task 1",
    "status": "pending",
    "due_date": "2025-05-28",
    "start_date": "2025-05-28",
    "assigned_to": 1,
    "project_id": 3,
    "description": "Task description"
  }
]
```

#### Delete Task
**Endpoint**: DELETE /delete-task/{task_id}  
**Description**: Deletes a task by ID

- Parameters
  - task_id = 4 (path)

**Response**
```json
{
  "message": "Task deleted successfully"
}
```

#### Update Task
**Endpoint**: PUT /update-task/{task_id}  
**Description**: Updates a task

- Parameters
  - task_id = 3 (path)

**Request**
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "status": "completed",
  "due_date": "2025-05-28",
  "start_date": "2025-05-28"
}
```

**Response**
```json
{
  "id": 3,
  "title": "Updated title",
  "status": "completed",
  "due_date": "2025-05-28",
  "start_date": "2025-05-28",
  "assigned_to": 1,
  "project_id": 3,
  "description": "Updated description"
}
```

### Attachments

#### Upload Attachment
**Endpoint**: POST /tasks/{task_id}/attachments  
**Description**: Uploads an attachment to a task

- Parameters
  - task_id = 3 (path)

**Request**
```json
{
  string($binary)
  .eml file data
}
```

**Response**
```json
{
  "filename": "Example mail.eml",
  "id": 9
}
```

#### Get Attachments
**Endpoint**: GET /tasks/{task_id}/attachments  
**Description**: Retrieves attachments for a task

- Parameters
  - task_id = 3 (path)

**Response**
```json
[
  {
    "id": 9,
    "filename": "Example Mail.eml",
    "task_id": 3,
    "created_at": "2025-05-28T09:54:47.162191"
  }
]
```

#### Download Attachment
**Endpoint**: GET /attachments/download/{attachment_id}  
**Description**: Downloads an attachment

- Parameters
  - attachment_id = 9 (path)

**Response**
- Downloadable File link

### Comment CRUD

#### Create Comment
**Endpoint**: POST /task/{task_id}  
**Description**: Creates a comment on a task

- Parameters
  - task_id = 3 (path)

**Request**
```json
{
  "content": "Example"
}
```

**Response**
```json
{
  "content": "Example",
  "id": 1,
  "user_id": 1,
  "task_id": 3,
  "created_at": "2025-05-28T10:02:26.724259",
  "user": {
    "id": 1,
    "username": "Samuel",
    "email": "samuelpleo79@gmail.com",
    "role": "admin"
  }
}
```

#### Get Comments
**Endpoint**: GET /task/{task_id}  
**Description**: Retrieves all comments for a task

**Response**
```json
[
  {
    "content": "Example",
    "id": 1,
    "user_id": 1,
    "task_id": 3,
    "created_at": "2025-05-28T10:02:26.724259",
    "user": {
      "id": 1,
      "username": "Samuel",
      "email": "samuelpleo79@gmail.com",
      "role": "admin"
    }
  }
]
```

#### Update Comment
**Endpoint**: PUT /comments/{comment_id}  
**Description**: Updates a comment

- Parameters
  - comment_id = 1 (path)

**Request**
```json
{
  "content": "Example Updated"
}
```

**Response**
```json
{
  "content": "Example Updated",
  "id": 1,
  "user_id": 1,
  "task_id": 3,
  "created_at": "2025-05-28T10:02:26.724259",
  "user": {
    "id": 1,
    "username": "Samuel",
    "email": "samuelpleo79@gmail.com",
    "role": "admin"
  }
}
```

#### Delete Comment
**Endpoint**: DELETE /{comment_id}  
**Description**: Deletes a comment

**Response**
- No content

### Summary

#### User Summary
**Endpoint**: GET /user-summary  
**Description**: Provides a summary for the user

**Response**
```json
{
  "username": 1,
  "assigned_tasks": 3,
  "completed_tasks": 1,
  "overdue_tasks": 2,
  "soon_due_tasks": 0
}
```

#### Project Summary
**Endpoint**: GET /project-summary  
**Description**: Provides a summary of all projects

**Response**
```json
[
  {
    "project_name": "Project 1",
    "total_tasks": 1,
    "completed_tasks": 0,
    "pending_tasks": 1
  },
  {
    "project_name": "Project 2",
    "total_tasks": 3,
    "completed_tasks": 1,
    "pending_tasks": 2
  }
]
```

#### Get Tasks by Status
**Endpoint**: GET /tasks/{status}  
**Description**: Retrieves tasks by status (assigned_tasks, completed, etc.)

**Response**
```json
[
  {
    "id": 2,
    "title": "Task 1",
    "status": "pending",
    "start_date": "2025-05-26",
    "project_id": 3,
    "description": "!",
    "due_date": "2025-05-27",
    "assigned_to": 1
  },
  {
    "id": 3,
    "title": "Updated title",
    "status": "completed",
    "start_date": "2025-05-28",
    "project_id": 3,
    "description": "Updated description",
    "due_date": "2025-05-28",
    "assigned_to": 1
  },
  {
    "id": 5,
    "title": "Task 1",
    "status": "pending",
    "start_date": "2025-05-28",
    "project_id": 3,
    "description": "Task description",
    "due_date": "2025-05-28",
    "assigned_to": 1
  }
]
```

## Developer

Made by SAM
