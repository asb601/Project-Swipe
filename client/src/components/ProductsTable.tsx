import {
  Table,
  TableBody,
  TableCaption,
  TableHead,
  TableHeader,
  TableRow,
  TableCell,
} from "@/components/ui/table";
import { useSelector } from "react-redux";
import { RootState } from "../redux/store";

export const ProductsTable = () => {
  const products = useSelector((state: RootState) => state.data.products);

  if (!products || products.length === 0) {
    return <div className="text-center m-3">No Products Found</div>;
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-center text-2xl font-semibold text-gray-800 mb-6">
        Products
      </h2>
      <Table className="w-full border border-gray-200 rounded-lg overflow-hidden">
        <TableCaption className="text-gray-500 text-sm">
          A list of recent products
        </TableCaption>
        <TableHeader className="bg-gray-100">
          <TableRow>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Product Name
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Quantity
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Unit Price
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Tax
            </TableHead>
            <TableHead className="text-left px-4 py-2 text-gray-700 font-semibold">
              Price with Tax
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {products.map((product: any, index: any) => (
            <TableRow
              key={index}
              className={`${
                index % 2 === 0 ? "bg-gray-50" : "bg-white"
              } hover:bg-gray-100 transition-colors`}
            >
              <TableCell className="px-4 py-2 text-gray-800">
                {product.productName}
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                {product.quantity}
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                ₹{product.unitPrice || "N/A"}
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                {product.tax}%
              </TableCell>
              <TableCell className="px-4 py-2 text-gray-800">
                ₹{product.priceWithTax}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
  
};
