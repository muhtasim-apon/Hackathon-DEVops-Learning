# MongoDB Learning Guide 🍃

Welcome to the MongoDB section of my Backend DevOps Learning journey! This folder contains MongoDB learning materials, connection examples, and practice scripts. 

---

## 📁 Folder Structure

```
MongoDB/
├── atlas_starter_nodejs/      # MongoDB Atlas connection examples
│   ├── app.js                 # Main application with CRUD operations
│   ├── package.json           # Node.js dependencies
│   └── node_modules/          # Installed packages
├── playground-1. mongodb.js    # VS Code MongoDB Playground scripts
├── commands. txt               # MongoDB shell commands reference
└── README.md                  # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** installed (v14 or higher)
- **MongoDB Atlas account** (free tier available at [mongodb.com](https://www.mongodb.com/cloud/atlas))
- **npm** package manager

### Installation

1. Navigate to the MongoDB folder:
   ```bash
   cd MongoDB/atlas_starter_nodejs
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file (recommended):
   ```bash
   MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/? retryWrites=true&w=majority
   ```

4. Run the application:
   ```bash
   node app.js
   ```

---

## 📚 MongoDB CRUD Operations

### Connect to MongoDB

```javascript
const { MongoClient } = require('mongodb');

const uri = "your-connection-string";
const client = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

await client.connect();
```

### Create (Insert) Documents

```javascript
// Insert one document
await collection.insertOne({
  username: "muhtasim-apon",
  email: "example@email.com"
});

// Insert multiple documents
await collection.insertMany([
  { name: "Document 1" },
  { name: "Document 2" }
]);
```

### Read (Find) Documents

```javascript
// Find all documents
const docs = await collection.find({}).toArray();

// Find with filter
const result = await collection.findOne({ username: "muhtasim-apon" });

// Find with conditions
const filtered = await collection.find({ age: { $gt: 25 } }).toArray();
```

### Update Documents

```javascript
// Update one document
await collection.updateOne(
  { username: "muhtasim-apon" },
  { $set: { email: "newemail@example.com" } }
);

// Update with returnDocument
await collection.findOneAndUpdate(
  { username: "muhtasim-apon" },
  { $set: { status: "active" } },
  { returnDocument: 'after' }
);
```

### Delete Documents

```javascript
// Delete one document
await collection.deleteOne({ username: "muhtasim-apon" });

// Delete multiple documents
await collection.deleteMany({ status: "inactive" });
```

---

## 🔧 Configuration

### Connection String Format

**MongoDB Atlas (Recommended):**
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb. net/? retryWrites=true&w=majority
```

**Local MongoDB:**
```
mongodb://localhost:27017/database_name
```

### Environment Variables (Best Practice)

Create a `.env` file:
```env
MONGODB_URI=your-connection-string
DB_NAME=your-database-name
```

Load in your app:
```javascript
require('dotenv').config();
const uri = process.env.MONGODB_URI;
```

---

## 📖 Common MongoDB Commands

### Database Operations
```javascript
// Show all databases
show dbs

// Switch to database
use myDatabase

// Show current database
db. getName()

// Drop database
db.dropDatabase()
```

### Collection Operations
```javascript
// Show all collections
show collections

// Create collection
db.createCollection("myCollection")

// Drop collection
db.myCollection.drop()
```

### Query Operations
```javascript
// Count documents
db.collection.countDocuments()

// Find with limit
db.collection.find().limit(10)

// Sort documents
db.collection.find().sort({ createdAt: -1 })

// Find with projection (select specific fields)
db.collection.find({}, { username: 1, email: 1, _id: 0 })
```

---

## 🛠️ Tools

### 1. MongoDB Compass (GUI)
- Download: [mongodb.com/products/compass](https://www.mongodb.com/products/compass)
- Visual interface for browsing and querying data
- Paste connection string to connect

### 2. MongoDB Shell (mongosh)
- Download: [mongodb.com/try/download/shell](https://www.mongodb.com/try/download/shell)
- Command-line interface for MongoDB
- Connect: `mongosh "your-connection-string"`

### 3. VS Code MongoDB Extension
- Install from VS Code Extensions marketplace
- Run playground scripts directly in VS Code
- Syntax highlighting for `. mongodb.js` files

---

## 🐛 Troubleshooting

### Issue: "Cannot find module 'mongodb'"
**Solution:**
```bash
npm install mongodb
```

### Issue: "Authentication failed"
**Solutions:**
1. Verify username and password in MongoDB Atlas
2. Reset database user password
3. Check if user has correct permissions
4. URL-encode special characters in password

### Issue: "Network timeout" or "Connection refused"
**Solutions:**
1. Add your IP address to MongoDB Atlas whitelist
2. Check internet connection
3. Verify connection string format

### Issue: Deprecation warnings
**Solution:** Update your MongoClient options:
```javascript
const client = new MongoClient(uri, {
  useNewUrlParser: true,
  useUnifiedTopology: true
});
```

---

## 🔒 Security Best Practices

1. **Never commit credentials** to Git
   - Use `. env` files
   - Add `. env` to `.gitignore`

2. **Use strong passwords** for database users

3. **Whitelist specific IP addresses** instead of `0.0.0.0/0`

4. **Hash passwords** before storing (use bcrypt):
   ```javascript
   const bcrypt = require('bcrypt');
   const hashedPassword = await bcrypt.hash(password, 10);
   ```

5. **Use environment-specific configurations**

---

## 📚 Learning Resources

- [MongoDB Official Documentation](https://docs.mongodb. com/)
- [MongoDB University (Free Courses)](https://university.mongodb. com/)
- [MongoDB Node.js Driver Docs](https://mongodb.github. io/node-mongodb-native/)
- [W3Schools MongoDB Tutorial](https://www.w3schools.com/mongodb/)

---

## 🎯 Practice Exercises

### Exercise 1: User Management System
Create a collection to store users with:
- Username
- Email
- Password (hashed)
- Registration date
- Active status

### Exercise 2: Recipe Database
Build a recipes collection with:
- Recipe name
- Ingredients array
- Preparation time
- Difficulty level
- Tags

### Exercise 3: Blog System
Design collections for:
- Posts (title, content, author, date)
- Comments (post reference, author, content)
- Categories

---

## 📝 Notes

- Always close MongoDB connections after operations
- Use `try-catch` blocks for error handling
- Index frequently queried fields for better performance
- Use aggregation pipeline for complex queries

---

## 🤝 Contributing

This is a personal learning repository, but suggestions are welcome! 

---

## 📄 License

This project is for educational purposes. 

---

**Happy Learning!  🚀**

*Last Updated: December 2, 2025*
