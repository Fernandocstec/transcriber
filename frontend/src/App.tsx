import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { VideoUploadForm } from './components/VideoUploadForm';
import { TranscriptionList } from './components/TranscriptionList';
import { TranscriptionDetails } from './components/TranscriptionDetails';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <Link to="/" className="text-xl font-bold text-gray-900">
                    Transcriber App
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <main className="py-10">
          <div className="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={
                <div className="space-y-8">
                  <VideoUploadForm />
                  <div className="bg-white shadow sm:rounded-lg p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      Recent Transcriptions
                    </h2>
                    <TranscriptionList />
                  </div>
                </div>
              } />
              <Route path="/transcripts/:id" element={<TranscriptionDetails />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
