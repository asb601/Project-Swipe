import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useSelector, useDispatch } from "react-redux";
import { RootState } from "../redux/store";
import { setActiveTab } from "../redux/dataSlice";


export const InvoicesTable = () => {
  const invoices = useSelector((state: RootState) => state.data.invoices);
  const dispatch = useDispatch();
  if (!invoices || invoices.length === 0) {
    return <div className="text-center m-3">No Invoices Found</div>;
  }

  // Group invoices by serialNumber
  const groupedInvoices = invoices.reduce((acc: any, invoice: any) => {
    if (!acc[invoice.serialNumber]) {
      acc[invoice.serialNumber] = {
        serialNumber: invoice.serialNumber,
        customerName: invoice.customerName,
        date: invoice.date,
        totalAmount: "0", // Initialize as a string
        products: [],
      };
    }
    // Add totalAmount as a string and ensure proper formatting
    const currentAmount = parseFloat(invoice.totalAmount || "0");
    const existingAmount = parseFloat(acc[invoice.serialNumber].totalAmount || "0");
    acc[invoice.serialNumber].totalAmount = (existingAmount + currentAmount).toFixed(2);
    acc[invoice.serialNumber].products.push({
      productName: invoice.productName,
      quantity: invoice.quantity,
      tax: invoice.tax,
      totalAmount: invoice.totalAmount,
    });
    return acc;
  }, {});

  const groupedData = Object.values(groupedInvoices);

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-center text-2xl font-semibold text-gray-800 mb-6">
        Invoices
      </h2>
      <Table className="w-full border border-gray-200 rounded-lg overflow-hidden">
        <TableCaption className="text-gray-500 text-sm">
          A list of recent invoices
        </TableCaption>
        <TableHeader className="bg-gray-100">
          <TableRow>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Serial Number
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Customer Name
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Date
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Total Amount
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Products
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {groupedData.map((invoice: any, index: any) => (
            <TableRow
              key={index}
              className={`${
                index % 2 === 0 ? "bg-gray-50" : "bg-white"
              } hover:bg-gray-100 transition-colors`}
            >
              <TableCell className="px-4 py-2 text-gray-800">
                {invoice.serialNumber}
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                {invoice.customerName}
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                {invoice.date}
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                ₹{invoice.totalAmount}
              </TableCell>
              <TableCell className="px-4 py-2">
                <button
                  className="text-blue-500 underline hover:text-blue-700 transition-colors"
                  onClick={() => {
                    // Dispatch to switch to the Products tab
                    dispatch(setActiveTab("products"));
                  }}
                >
                  View Products
                </button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
  
};
