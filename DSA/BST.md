## Traversal Node

- Preorder = (root -> left -> right)
- Inorder = (left -> root -> right)
- Postorder = (left -> right -> root)

```c++
#include <iostream>
#include <vector>
using namespace std;

struct Node
{
    int data;
    Node* left;
    Node* right;

    Node(int val)
    {
        data = val;
        left = nullptr;
        right = nullptr;
    }
};

void preorder(Node* root)
{
    if(root == nullptr) return;

    cout << root->data << " ";

    preorder(root->left);
    preorder(root->right);
}

void inorder(Node* root)
{
    if(root == nullptr) return;

    inorder(root -> left);
    cout<<root -> data<<" ";
    inorder(root -> right);
}

void postorder(Node* root)
{
    if(root == nullptr) return;

    postorder(root -> left);
    postorder(root -> right);
    cout<<root -> data<<" ";
}

int main()
{
    Node* root = new Node(1);
    root -> left = new Node(2);
    root -> right = new Node(3);
    root -> left -> left = new Node(4);
    root -> left -> right = new Node(5);
    root -> right -> left = new Node(10);

    cout<<"Preorder Traversal: ";
    preorder(root);
    cout<<endl;

    cout<<"Inorder Traversal: ";
    inorder(root);
    cout<<endl;

    cout<<"Postorder Traversal: ";
    postorder(root);
    cout<<endl;

    // Clean up memory (optional for this example)
    delete root->left->left;
    delete root->left->right;
    delete root->right->right;
    delete root->left;
    delete root->right;
    delete root;

    return 0;
}
```

```text
      1
     / \
    2   3
   / \   \
  4   5   6
```

```text
Preorder traversal: 1 2 4 5 3 6 
Inorder traversal: 4 2 5 1 3 6 
Postorder traversal: 4 5 2 6 3 1 
```

**Time Complexity**: Each traversal visits every node exactly once, so the time complexity is O(n), where n is the number of nodes.
**Space Complexity**: O(h) due to the recursion stack, where h is the height of the tree.

## BST Operations 
- **Insert**: Add a new node with a given value, maintaining BST property (left child < node < right child).
- **Delete**: Remove a node with a given value, restructuring the tree to maintain BST property.
- **Search**: Find a node with a given value.
- **Successor**: Find the node with the smallest value greater than a given node.
- **Predecessor**: Find the node with the largest value less than a given node.
- **Maximum**: Find the node with the largest value in the tree.
- **Minimum**: Find the node with the smallest value in the tree.

```c++
#include <iostream>
using namespace std;

// Definition of a BST node
struct Node 
{
    int data;
    Node* left;
    Node* right;
    Node* parent;  // For successor/predecessor operations

    Node(int val) 
    {
        data = val;
        left = nullptr;
        right = nullptr;
        parent = nullptr;
    }
};

class BST {
private:
    Node* root;

    // Helper function for recursive insertion
    Node* insertRec(Node* node, int val, Node* parent) 
    {
        if (node == nullptr) {
            Node* newNode = new Node(val);
            newNode->parent = parent;
            return newNode;
        }
        if (val < node->data) 
        {
            node->left = insertRec(node->left, val, node);
        } 
        else if (val > node->data) 
        {
            node->right = insertRec(node->right, val, node);
        }
        return node;
    }

    // Helper function for recursive search
    Node* searchRec(Node* node, int val) 
    {
        if (node == nullptr || node->data == val) return node;
        if (val < node->data) return searchRec(node->left, val);
        return searchRec(node->right, val);
    }

    // Helper function to find the minimum node in a subtree
    Node* findMin(Node* node) 
    {
        if (node == nullptr) return nullptr;
        while (node->left) node = node->left;
        return node;
    }

    // Helper function to find the maximum node in a subtree
    Node* findMax(Node* node) 
    {
        if (node == nullptr) return nullptr;
        while (node->right) node = node->right;
        return node;
    }

    // Helper function to find the successor of a node
    Node* findSuccessor(Node* node) 
    {
        if (node == nullptr) return nullptr;
        // Case 1: Node has a right child
        if (node->right) return findMin(node->right);
        // Case 2: No right child, go up until we find a parent whose left child we are
        Node* curr = node;
        while (curr->parent && curr == curr->parent->right) {
            curr = curr->parent;
        }
        return curr->parent;  // Could be nullptr if no successor
    }

    // Helper function to find the predecessor of a node
    Node* findPredecessor(Node* node) 
    {
        if (node == nullptr) return nullptr;
        // Case 1: Node has a left child
        if (node->left) return findMax(node->left);
        // Case 2: No left child, go up until we find a parent whose right child we are
        Node* curr = node;
        while (curr->parent && curr == curr->parent->left) {
            curr = curr->parent;
        }
        return curr->parent;  // Could be nullptr if no predecessor
    }

    // Helper function for deletion
    Node* deleteRec(Node* node, int val) 
    {
        if (node == nullptr) return nullptr;

        if (val < node->data) 
        {
            node->left = deleteRec(node->left, val);
        } 
        else if (val > node->data) 
        {
            node->right = deleteRec(node->right, val);
        } 
        else 
        {
            // Node to delete found
            // Case 1: Leaf node
            if (node->left == nullptr && node->right == nullptr) {
                delete node;
                return nullptr;
            }
            // Case 2: Node with only one child
            if (node->left == nullptr) 
            {
                Node* temp = node->right;
                temp->parent = node->parent;
                delete node;
                return temp;
            }
            
            if (node->right == nullptr) 
            {
                Node* temp = node->left;
                temp->parent = node->parent;
                delete node;
                return temp;
            }
            // Case 3: Node with two children
            Node* succ = findMin(node->right);  // Successor (smallest in right subtree)
            node->data = succ->data;  // Replace node's value with successor's
            node->right = deleteRec(node->right, succ->data);  // Delete successor
        }
        return node;
    }

    // Helper function for inorder traversal (to display the tree)
    void inorderRec(Node* node) 
    {
        if (node == nullptr) return;
        inorderRec(node->left);
        cout << node->data << " ";
        inorderRec(node->right);
    }

public:
    BST() 
    {
        root = nullptr;
    }

    // Insert a value into the BST
    void insert(int val) 
    {
        root = insertRec(root, val, nullptr);
    }

    // Search for a value in the BST
    Node* search(int val) 
    {
        return searchRec(root, val);
    }

    // Delete a value from the BST
    void remove(int val) 
    {
        root = deleteRec(root, val);
    }

    // Find the minimum value in the BST
    Node* minimum() 
    {
        return findMin(root);
    }

    // Find the maximum value in the BST
    Node* maximum() 
    {
        return findMax(root);
    }

    // Find the successor of a given value
    Node* successor(int val) 
    {
        Node* node = search(val);
        if (node == nullptr) return nullptr;
        return findSuccessor(node);
    }

    // Find the predecessor of a given value
    Node* predecessor(int val) 
    {
        Node* node = search(val);
        if (node == nullptr) return nullptr;
        return findPredecessor(node);
    }

    // Display the tree in inorder (for verification)
    void displayInorder() 
    {
        inorderRec(root);
        cout << endl;
    }
};

int main() 
{
    BST tree;

    // Insert some values
    tree.insert(50);
    tree.insert(30);
    tree.insert(70);
    tree.insert(20);
    tree.insert(40);
    tree.insert(60);
    tree.insert(80);

    // Display the tree in inorder (should be sorted)
    cout << "Inorder traversal of the BST: ";
    tree.displayInorder();  // Expected: 20 30 40 50 60 70 80

    // Search for a value
    int val = 40;
    Node* found = tree.search(val);
    cout << "Search for " << val << ": " << (found ? "Found" : "Not Found") << endl;

    // Find minimum and maximum
    Node* min = tree.minimum();
    Node* max = tree.maximum();
    cout << "Minimum: " << (min ? min->data : -1) << endl;  // Expected: 20
    cout << "Maximum: " << (max ? max->data : -1) << endl;  // Expected: 80

    // Find successor and predecessor
    val = 30;
    Node* succ = tree.successor(val);
    Node* pred = tree.predecessor(val);
    cout << "Successor of " << val << ": " << (succ ? succ->data : -1) << endl;  // Expected: 40
    cout << "Predecessor of " << val << ": " << (pred ? pred->data : -1) << endl;  // Expected: 20

    // Delete a value and display the tree again
    tree.remove(30);
    cout << "Inorder traversal after deleting 30: ";
    tree.displayInorder();  // Expected: 20 40 50 60 70 80

    return 0;
}
```

1. **Insert**:
    - Recursively traverse to the correct position based on the BST property.
    - Set the parent pointer for the new node.
2. **Search**:
    - Recursively traverse based on the value, return the node if found, or nullptr if not.
3. **Delete**:
    - Handles three cases:
        - Leaf node: Simply remove it.
        - One child: Replace the node with its child.
        - Two children: Replace the node’s value with its successor’s value, then delete the successor.
4. **Find Minimum/Maximum**:
    - Minimum: Traverse to the leftmost node.
    - Maximum: Traverse to the rightmost node.
5. **Find Successor**:
    - If the node has a right child, the successor is the leftmost node in the right subtree.
    - Otherwise, go up until you find a node that is a left child of its parent.
6. **Find Predecessor**:
    - If the node has a left child, the predecessor is the rightmost node in the left subtree.
    - Otherwise, go up until you find a node that is a right child of its parent.
7. **Example in main**:
    - Builds a BST with values: 50, 30, 70, 20, 40, 60, 80.
    - The tree looks like:
        
  
```text
      50
     /  \
   30    70
  /  \   /  \
 20  40 60   80
```

```text
Inorder traversal of the BST: 20 30 40 50 60 70 80 
Search for 40: Found
Minimum: 20
Maximum: 80
Successor of 30: 40
Predecessor of 30: 20
Inorder traversal after deleting 30: 20 40 50 60 70 80 
```

### Time Complexity

- **Insert, Search, Delete**: O(h), where h is the height of the tree (O(log n) for a balanced tree, O(n) for a skewed tree).
- **Find Min/Max, Successor/Predecessor**: O(h), same as above.
- **Space Complexity**: O(h) due to recursion stack.

Inorder DFS
- Naturally visits nodes in sorted order
- left -> root -> right
- so the k-th node you visit is the k-th smallest 
- no sorting needed