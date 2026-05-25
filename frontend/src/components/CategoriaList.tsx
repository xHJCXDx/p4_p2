import { Categoria } from '../types/categoria';

interface Props {
  categorias: Categoria[];
  onEdit: (categoria: Categoria) => void;
  onDelete: (id: number) => void;
}

const CategoriaList = ({ categorias, onEdit, onDelete }: Props) => {
  return (
    <div className="overflow-x-auto bg-white rounded-lg shadow">
      <table className="w-full">
        <thead className="bg-gray-200 border-b-2 border-gray-300">
          <tr>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">NÚMERO</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">NOMBRE</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">DESCRIPCIÓN</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">ACCIONES</th>
          </tr>
        </thead>
        <tbody>
          {categorias.map((cat) => (
            <tr key={cat.id} className="border-b border-gray-200 hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4 text-sm text-gray-700">{cat.id}</td>
              <td className="px-6 py-4 text-sm font-medium text-gray-900">{cat.nombre}</td>
              <td className="px-6 py-4 text-sm text-gray-600">{cat.descripcion}</td>
              <td className="px-6 py-4 text-sm space-x-2 flex">
                <button
                  onClick={() => onEdit(cat)}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition-colors font-medium"
                >
                  Editar
                </button>
                <button
                  onClick={() => cat.id && onDelete(cat.id)}
                  className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition-colors font-medium"
                >
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CategoriaList;
