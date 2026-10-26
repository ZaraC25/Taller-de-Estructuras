from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CLASES DEL PDF (Páginas 21-23) ---
class Node:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.left = None
        self.right = None

class Phonebook:
    def __init__(self):
        self.root = None

    def insert(self, name, phone_number):
        new_node = Node(name, phone_number)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if name < current.name:
                    if current.left is None:
                        current.left = new_node
                        break
                    else:
                        current = current.left
                elif name > current.name:
                    if current.right is None:
                        current.right = new_node
                        break
                    else:
                        current = current.right
                else:
                    current.phone_number = phone_number # Actualiza si ya existe
                    break

    def search(self, name):
        current = self.root
        while current is not None:
            if name == current.name:
                return current.phone_number
            elif name < current.name:
                current = current.left
            else:
                current = current.right
        return None

    # Método extra para convertir el árbol a diccionario y enviarlo al Frontend
    def get_tree_structure(self, node):
        if node is None:
            return None
        return {
            "name": node.name,
            "phone": node.phone_number,
            "children": [
                self.get_tree_structure(node.left),
                self.get_tree_structure(node.right)
            ]
        }

# Instancia global de la agenda
agenda = Phonebook()

# --- RUTAS DE FLASK ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/add', methods=['POST'])
def add_contact():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    if name and phone:
        agenda.insert(name, phone)
        return jsonify({"status": "success", "message": "Contacto guardado"})
    return jsonify({"status": "error", "message": "Faltan datos"}), 400

@app.route('/api/search', methods=['GET'])
def search_contact():
    name = request.args.get('name')
    if name:
        phone = agenda.search(name)
        if phone:
            return jsonify({"status": "found", "phone": phone})
        return jsonify({"status": "not_found", "message": "Contacto no encontrado"})
    return jsonify({"status": "error", "message": "Nombre no proporcionado"}), 400

@app.route('/api/tree', methods=['GET'])
def get_tree():
    # Retorna la estructura para que D3.js la dibuje
    tree_data = agenda.get_tree_structure(agenda.root)
    return jsonify(tree_data)

if __name__ == '__main__':
    # Insertamos algunos datos de ejemplo iniciales
    agenda.insert("Jhonatan", "111-1111")
    agenda.insert("Andrea", "222-2222")
    agenda.insert("Carlos", "333-3333")
    agenda.insert("Diana", "444-4444")
    agenda.insert("Ivan", "555-5555")
    
    app.run(debug=True)
