import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Provider } from "react-redux"; // Import Provider from react-redux
import HomePage from "./pages/HomePage";
import store from "./redux/store"; // Import the Redux store

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  );
}

export default App;
