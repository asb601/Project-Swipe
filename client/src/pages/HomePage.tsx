import { CustomersTable } from "@/components/CustomersTable";
import { InvoicesTable } from "@/components/InvoicesTable";
import { Navbar } from "@/components/Navbar";
import { ProductsTable } from "@/components/ProductsTable";
import { Input } from "@/components/ui/input";
import { useDispatch, useSelector } from "react-redux";
import { setData, setActiveTab } from "../redux/dataSlice";
import { RootState } from "../redux/store";

export default function HomePage() {
  const dispatch = useDispatch();
  const { invoices, products, customers, activeTab } = useSelector((state: RootState) => state.data);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("https://project-swipe.onrender.com/process-invoice", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process the file");
      }

      const result = await response.json();
     
      dispatch(setData(result));
      console.log("Redux State After Update:", { invoices, products, customers });

      console.log("Redux State After Update:", result) // Store data in Redux
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
  
      <div className="container mx-auto p-6">
        {/* File Upload */}
        <div className="mb-6 flex items-center space-x-4">
          <label
            htmlFor="file-upload"
            className="block text-lg font-medium text-gray-700"
          >
            Upload Invoice:
          </label>
          <Input
            id="file-upload"
            type="file"
            className="w-full max-w-xs rounded border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            onChange={handleFileUpload}
          />
        </div>
  
        {/* Tabs */}
        <div className="mb-6 flex gap-10 border-b border-gray-200">
          <div
            onClick={() => dispatch(setActiveTab("invoices"))}
            className={`cursor-pointer px-4 py-2 text-lg font-semibold ${
              activeTab === "invoices"
                ? "border-b-2 border-blue-500 text-blue-500"
                : "text-gray-600 hover:text-blue-500"
            }`}
          >
            Invoices
          </div>
          <div
            onClick={() => dispatch(setActiveTab("products"))}
            className={`cursor-pointer px-4 py-2 text-lg font-semibold ${
              activeTab === "products"
                ? "border-b-2 border-blue-500 text-blue-500"
                : "text-gray-600 hover:text-blue-500"
            }`}
          >
            Products
          </div>
          <div
            onClick={() => dispatch(setActiveTab("customers"))}
            className={`cursor-pointer px-4 py-2 text-lg font-semibold ${
              activeTab === "customers"
                ? "border-b-2 border-blue-500 text-blue-500"
                : "text-gray-600 hover:text-blue-500"
            }`}
          >
            Customers
          </div>
        </div>
  
        {/* Dynamic Rendering Based on Selected Tab */}
        <div className="bg-white rounded-lg shadow-md p-6">
          {activeTab === "invoices" && <InvoicesTable />}
          {activeTab === "products" && <ProductsTable />}
          {activeTab === "customers" && (
            <CustomersTable onTabChange={(tab: string) => dispatch(setActiveTab(tab))} />
          )}
        </div>
      </div>
    </div>
  );
  
}
