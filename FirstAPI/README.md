# FastAPI Todo Application with MongoDB

A professional todo application built with FastAPI and MongoDB Atlas, featuring a modern UI and complete CRUD operations.

## 🚀 Features

- ✅ Full CRUD operations for todos
- 🗄️ MongoDB Atlas integration
- 📊 Real-time statistics dashboard
- 🔍 Search and filter functionality
- 🎨 Modern, responsive UI
- 🔄 In-memory fallback when database is unavailable
- 🏥 Health check endpoints
- 📝 Interactive API documentation (Swagger/OpenAPI)

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB)
- pip (Python package manager)

## 🛠️ Installation

1. **Clone or download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure database connection**
   - Open `database.py`
   - Update the MongoDB credentials:
     ```python
     username = "your_username"
     password = "your_password"
     ```

## 🏃 Running the Application

### Start the server:
```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

### Access the application:
- **Homepage**: http://127.0.0.1:8000
- **Todo Manager**: http://127.0.0.1:8000/todos
- **API Documentation**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/api/health

## 📚 API Endpoints

### Todos
- `GET /api/todos` - Get all todos (with filters)
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a todo
- `DELETE /api/todos/{id}` - Delete a todo
- `PATCH /api/todos/{id}/toggle` - Toggle todo completion

### Statistics
- `GET /api/stats` - Get todo statistics
- `GET /api/todos/search?keyword={text}` - Search todos

### System
- `GET /api/health` - Health check
- `GET /api/db-info` - Database connection info
- `GET /api` - API root information

## 🗄️ Database Structure

### Todo Schema
```json
{
  "_id": "ObjectId",
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (default: false)",
  "priority": "string (low/medium/high)",
  "created_at": "datetime"
}
```

## 🎯 Usage Examples

### Create a Todo (cURL)
```bash
curl -X POST "http://127.0.0.1:8000/api/todos" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the FastAPI todo app",
    "priority": "high"
  }'
```

### Get All Todos
```bash
curl "http://127.0.0.1:8000/api/todos"
```

### Filter Todos
```bash
curl "http://127.0.0.1:8000/api/todos?completed=false&priority=high"
```

## 🔧 Configuration

### MongoDB Connection
Edit `database.py` to configure your MongoDB connection:
- Username
- Password
- Cluster URL
- Database name

### Server Settings
Edit `main.py` to change server settings:
```python
uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

## 📦 Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **PyMongo**: MongoDB driver
- **Pydantic**: Data validation
- **Jinja2**: Template engine
- **python-multipart**: Form data parsing

## 🛡️ Error Handling

The application includes comprehensive error handling:
- Database connection failures → Falls back to in-memory storage
- Invalid todo IDs → Returns 400 Bad Request
- Not found errors → Returns 404 Not Found
- Validation errors → Returns 422 Unprocessable Entity

## 🎨 Frontend Features

- Real-time todo updates
- Keyboard shortcuts (Ctrl+K for search, Shift+Enter to quick add)
- Filter by completion status and priority
- Search functionality
- Statistics dashboard
- Responsive design

## 🔒 Security Notes

⚠️ **Important for Production:**
1. Never commit credentials to version control
2. Use environment variables for sensitive data
3. Remove `tlsAllowInvalidCertificates=True` in production
4. Implement authentication and authorization
5. Add rate limiting
6. Use HTTPS

## 📈 Monitoring

Check application health:
```bash
curl http://127.0.0.1:8000/api/health
```

Check database info:
```bash
curl http://127.0.0.1:8000/api/db-info
```

## 🐛 Troubleshooting

### Database Connection Issues
- Verify MongoDB Atlas credentials
- Check IP whitelist in MongoDB Atlas
- Ensure network connectivity
- Check firewall settings

### Application Won't Start
- Verify Python version (3.8+)
- Install all dependencies: `pip install -r requirements.txt`
- Check if port 8000 is available

### In-Memory Mode
If you see "Using in-memory storage", the database connection failed. Check:
- MongoDB credentials in `database.py`
- Network connectivity
- MongoDB Atlas cluster status

## 📝 License

This project is open source and available under the MIT License.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on the project repository.

---

**Built with ❤️ using FastAPI and MongoDB**

