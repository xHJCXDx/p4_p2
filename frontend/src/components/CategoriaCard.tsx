import { Categoria } from '../types/categoria';

interface Props {
  categoria: Categoria;
  onEdit: (categoria: Categoria) => void;
  onDelete: (id: number) => void;
}

const CategoriaCard = ({ categoria, onEdit, onDelete }: Props) => {
  return (
    <div className="bg-white border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      <h3 className="text-xl font-semibold mb-2">{categoria.nombre}</h3>
      <p className="text-gray-600 mb-4">{categoria.descripcion}</p>
      <div className="flex justify-end space-x-2">
        <button
          onClick={() => onEdit(categoria)}
          className="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded transition-colors"
        >
          Editar
        </button>
        <button
          onClick={() => categoria.id && onDelete(categoria.id)}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition-colors"
        >
          Eliminar
        </button>
      </div>
    </div>
  );
};

export default CategoriaCard;
