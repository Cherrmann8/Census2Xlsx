import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders census2xlsx title in the header", () => {
  render(<App />);
  const titleElement = screen.getByText("Census2Xlsx")
  expect(titleElement).toBeInTheDocument();
});
