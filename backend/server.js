const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/openreview';
const PORT = process.env.PORT || 5000;

// Connect to MongoDB
mongoose.connect(MONGO_URI)
  .then(() => console.log('MongoDB Connected Successfully over internal network!'))
  .catch(err => console.error('Database connection error:', err));

// Simple Review Schema
const SubmissionSchema = new mongoose.Schema({
  title: String,
  author: String,
  reviewStatus: { type: String, default: 'Pending Review' }
});
const Submission = mongoose.model('Submission', SubmissionSchema);

// API Routes
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'Backend API is healthy and reachable' });
});

app.get('/api/submissions', async (req, res) => {
  try {
    const data = await Submission.find();
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/submissions', async (req, res) => {
  try {
    const newDoc = new Submission(req.body);
    await newDoc.save();
    res.status(201).json(newDoc);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});