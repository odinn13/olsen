head = Node("A", Node("B", Node("C", Node("D", None))))

node = head
if node != None:
   while node.next != None:
       node = node.next
node.next = head
head = head.next
node.next.next = None

print_list(head)
