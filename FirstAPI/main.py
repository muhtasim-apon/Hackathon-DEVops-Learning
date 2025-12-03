from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId

# Import database (if you have database.py)
try:
    from database import db, todos_collection, check_connection, get_db_info
    DB_CONNECTED = db is not None
except ImportError:
    DB_CONNECTED = False
    db = None
    todos_collection = None
    check_connection = lambda: False
    get_db_info = lambda: {"connected": False}
    print("⚠️ Running without database - using in-memory storage")

app = FastAPI(
    title="FastAPI with MongoDB",
    description="Backend with MongoDB Atlas integration",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory storage (fallback if DB not connected)
todos_memory = []


# ==================== DATA MODELS ====================
class Todo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None


# ==================== HTML ROUTES ====================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Homepage"""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"title": "Home", "message": "Welcome to FastAPI with MongoDB"}
    )


@app.get("/todos", response_class=HTMLResponse)
async def todos_page(request: Request):
    """Todos management page"""
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={"title": "Todos"}
    )


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item_html(request: Request, id: str):
    """Item detail page"""
    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={"id": id}
    )


# ==================== API ROUTES ====================
@app.get("/api")
async def api_root():
    return {
        "message": "FastAPI with MongoDB",
        "database_status": "connected" if DB_CONNECTED else "disconnected",
        "endpoints": {
            "todos": "/api/todos",
            "docs": "/docs",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    db_status = "disconnected"

    if DB_CONNECTED:
        try:
            if check_connection():
                db_status = "connected"
            else:
                db_status = "error"
        except:
            db_status = "error"

    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/db-info")
async def database_info():
    """Get detailed database information"""
    if not DB_CONNECTED:
        return {
            "status": "disconnected",
            "message": "Database is not connected. Using in-memory storage."
        }

    return get_db_info()


# ==================== TODO CRUD WITH MONGODB ====================

@app.post("/api/todos")
async def create_todo(todo: Todo):
    """Create a new todo"""
    if DB_CONNECTED and todos_collection is not None:
        # MongoDB storage
        todo_dict = todo.model_dump()
        todo_dict["created_at"] = datetime.now(timezone.utc)

        result = todos_collection.insert_one(todo_dict)
        todo_dict["_id"] = str(result.inserted_id)

        return {
            "message": "Todo created successfully",
            "todo": todo_dict
        }
    else:
        # In-memory storage (fallback)
        todo_dict = todo.model_dump()
        todo_dict["_id"] = str(len(todos_memory) + 1)
        todo_dict["created_at"] = datetime.now(timezone.utc).isoformat()
        todos_memory.append(todo_dict)

        return {
            "message": "Todo created successfully (in-memory)",
            "todo": todo_dict
        }


@app.get("/api/todos")
async def get_todos(
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        limit: int = 100
):
    """Get all todos with optional filters"""
    if DB_CONNECTED and todos_collection is not None:
        # MongoDB query
        query = {}
        if completed is not None:
            query["completed"] = completed
        if priority:
            query["priority"] = priority

        todos = list(todos_collection.find(query).limit(limit))

        # Convert ObjectId to string
        for todo in todos:
            todo["_id"] = str(todo["_id"])

        return {
            "total": len(todos),
            "todos": todos
        }
    else:
        # In-memory query
        todos = todos_memory

        if completed is not None:
            todos = [t for t in todos if t.get("completed") == completed]
        if priority:
            todos = [t for t in todos if t.get("priority") == priority]

        return {
            "total": len(todos),
            "todos": todos[:limit]
        }


@app.get("/api/todos/{todo_id}")
async def get_todo(todo_id: str):
    """Get a specific todo by ID"""
    if DB_CONNECTED and todos_collection is not None:
        try:
            todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
            if todo:
                todo["_id"] = str(todo["_id"])
                return todo
            raise HTTPException(status_code=404, detail="Todo not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid todo ID: {str(e)}")
    else:
        # In-memory query
        for todo in todos_memory:
            if todo["_id"] == todo_id:
                return todo
        raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/api/todos/{todo_id}")
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    """Update a todo"""
    if DB_CONNECTED and todos_collection is not None:
        try:
            update_data = {k: v for k, v in todo_update.model_dump().items() if v is not None}

            if not update_data:
                raise HTTPException(status_code=400, detail="No fields to update")

            result = todos_collection.update_one(
                {"_id": ObjectId(todo_id)},
                {"$set": update_data}
            )

            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail="Todo not found")

            updated_todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
            updated_todo["_id"] = str(updated_todo["_id"])

            return {
                "message": "Todo updated successfully",
                "todo": updated_todo
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid todo ID: {str(e)}")
    else:
        # In-memory update
        for i, todo in enumerate(todos_memory):
            if todo["_id"] == todo_id:
                update_data = {k: v for k, v in todo_update.model_dump().items() if v is not None}
                todos_memory[i].update(update_data)
                return {
                    "message": "Todo updated successfully",
                    "todo": todos_memory[i]
                }
        raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/api/todos/{todo_id}")
async def delete_todo(todo_id: str):
    """Delete a todo"""
    if DB_CONNECTED and todos_collection is not None:
        try:
            result = todos_collection.delete_one({"_id": ObjectId(todo_id)})

            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Todo not found")

            return {"message": "Todo deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid todo ID: {str(e)}")
    else:
        # In-memory delete
        global todos_memory
        initial_length = len(todos_memory)
        todos_memory = [t for t in todos_memory if t["_id"] != todo_id]

        if len(todos_memory) < initial_length:
            return {"message": "Todo deleted successfully"}
        raise HTTPException(status_code=404, detail="Todo not found")


@app.patch("/api/todos/{todo_id}/toggle")
async def toggle_todo(todo_id: str):
    """Toggle todo completion status"""
    if DB_CONNECTED and todos_collection is not None:
        try:
            todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
            if not todo:
                raise HTTPException(status_code=404, detail="Todo not found")

            new_status = not todo.get("completed", False)

            todos_collection.update_one(
                {"_id": ObjectId(todo_id)},
                {"$set": {"completed": new_status}}
            )

            updated_todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
            updated_todo["_id"] = str(updated_todo["_id"])

            return {
                "message": "Todo status toggled",
                "todo": updated_todo
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid todo ID: {str(e)}")
    else:
        # In-memory toggle
        for todo in todos_memory:
            if todo["_id"] == todo_id:
                todo["completed"] = not todo.get("completed", False)
                return {
                    "message": "Todo status toggled",
                    "todo": todo
                }
        raise HTTPException(status_code=404, detail="Todo not found")


# ==================== STATISTICS ====================
@app.get("/api/stats")
async def get_stats():
    """Get todo statistics"""
    if DB_CONNECTED and todos_collection is not None:
        total = todos_collection.count_documents({})
        completed = todos_collection.count_documents({"completed": True})
        pending = total - completed

        priority_stats = {
            "high": todos_collection.count_documents({"priority": "high"}),
            "medium": todos_collection.count_documents({"priority": "medium"}),
            "low": todos_collection.count_documents({"priority": "low"})
        }

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": priority_stats
        }
    else:
        # In-memory stats
        total = len(todos_memory)
        completed = len([t for t in todos_memory if t.get("completed")])
        pending = total - completed

        priority_stats = {
            "high": len([t for t in todos_memory if t.get("priority") == "high"]),
            "medium": len([t for t in todos_memory if t.get("priority") == "medium"]),
            "low": len([t for t in todos_memory if t.get("priority") == "low"])
        }

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": priority_stats
        }


@app.get("/api/todos/search")
async def search_todos(keyword: str):
    """Search todos by keyword"""
    if DB_CONNECTED and todos_collection is not None:
        results = list(todos_collection.find({
            "$or": [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"description": {"$regex": keyword, "$options": "i"}}
            ]
        }))

        for result in results:
            result["_id"] = str(result["_id"])

        return {
            "keyword": keyword,
            "count": len(results),
            "results": results
        }
    else:
        # In-memory search
        keyword_lower = keyword.lower()
        results = [
            t for t in todos_memory
            if keyword_lower in t.get("title", "").lower()
               or keyword_lower in t.get("description", "").lower()
        ]

        return {
            "keyword": keyword,
            "count": len(results),
            "results": results
        }


# ==================== RUN ====================
if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 50)
    print("🚀 Starting FastAPI Server")
    print("=" * 50)
    print(f"📦 Database: {'Connected to MongoDB ✅' if DB_CONNECTED else 'Using in-memory storage ⚠️'}")
    print(f"🌐 Homepage: http://127.0.0.1:8000")
    print(f"📋 Todos: http://127.0.0.1:8000/todos")
    print(f"📚 API Docs: http://127.0.0.1:8000/docs")
    print("=" * 50 + "\n")

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)