# 🛰️ AI Resume & JD Scanner

A full-stack web application designed to analyze the alignment between a candidate's resume and a job description using **Natural Language Processing (NLP)**.

## 🚀 Core Features
* **Automated Text Sanitization:** Utilizes `spaCy` for tokenization, stop-word removal, and lemmatization to extract core meaning from unstructured text.
* **ML-Powered Analysis:** Implements `Scikit-Learn`'s **TF-IDF Vectorization** and **Cosine Similarity** to calculate a mathematical match percentage.
* **Gap Identification:** Automatically detects "Missing Skills" by performing set-difference analysis on the semantic features of the JD and the resume.
* **Real-time API:** Powered by **FastAPI** for high-performance, asynchronous processing and response handling.

## 🛠️ Tech Stack
* **Frontend:** React (Vite), TypeScript, React Router
* **Backend:** Python, FastAPI, Uvicorn
* **Machine Learning:** spaCy (`en_core_web_md`), Scikit-Learn



## 🔧 Installation & Setup
1. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_md
   uvicorn main:app --reload
   ```

1. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 🧪 Testing

### Frontend Testing (Jest + React Testing Library)

**Installation (Already Done):**
```bash
cd frontend
npm install --save-dev jest @testing-library/react @testing-library/jest-dom jest-environment-jsdom @babel/preset-react @babel/preset-typescript identity-obj-proxy @types/jest ts-jest
```

**Test Setup:**
- Testing framework: **Jest** with **React Testing Library**
- Test files location: `frontend/tests/`
- Configuration: `frontend/jest.config.js`

**Test Structure:**
```
frontend/
├── tests/
│   ├── pages/
│   │   ├── HomePage.test.tsx
│   │   └── ResultPage.test.tsx
│   └── setup/
│       └── setupTests.ts
├── jest.config.js
└── TESTING.md (detailed guide)
```

**Running Tests:**
```bash
cd frontend

# Run all tests once
npm test

# Run tests in watch mode (auto-rerun on file changes)
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# Run specific test file
npm test -- HomePage

# Run tests matching a pattern
npm test -- --testNamePattern="validation"
```

**Current Test Coverage:**
- ✅ HomePage: 9 tests (form inputs, validation, submissions)
- ✅ ResultPage: 3 tests (empty state, navigation, button interactions)
- **Total: 12 passing tests**

**Writing New Tests:**
1. Create test file in `tests/` folder mirroring `src/` structure
2. Example: `tests/components/Button.test.tsx` for `src/components/Button.tsx`
3. Use relative imports: `import Button from '../../src/components/Button'`
4. See `TESTING.md` for patterns and best practices

### Backend Testing

```bash
cd backend

# Run tests
pytest tests/

# Run with coverage
pytest --cov=. tests/
```

