from dag import DAG, ImutablePath
from santa import Constraints
from random import shuffle
from IPython import embed
def allocate(participants, constraints=Constraints()):
	# first construct the DAG with the constraints
	dag = DAG()
	for giver in participants:
		for taker in participants:
			if constraints.is_allowed(giver,taker):
				dag.connect(dag.node(giver),dag.node(taker))
	completed = allocate_loop(dag)
	pairs = extract_pairs(completed)

	return pairs

def extract_pairs(completed):
	pairs = {}
	first = completed.current
	current = completed.children(first)[0]
	pairs[first.obj] = current.obj
	# print "%s -> %s"%(first.obj, current.obj)
	while current is not first:
		next = completed.children(current)[0]
		# print "%s -> %s"%(current.obj, next.obj)
		pairs[current.obj] = next.obj
		current = next
	return pairs

	
def allocate_loop(dag,path=ImutablePath(),given=[]):
	# print "Path Edge size: ", path.edgesize()
	if path.edgesize() == dag.size(): 
		return path

	nodes = None
	if path.current is None:
		nodes = dag.nodes()
	else:
		nodes = dag.children(path.current)

	nodes = list((set(nodes) - set(path.nodes())) | set(path.parentless_nodes()))

	shuffle(nodes)
	for node in nodes:
		p = path.iadd(node)
		if not valid_path(p, dag.size()):
			continue
		ret = allocate_loop(dag,p)
		if ret is not None:
			return ret
	return None

"""Valid paths:
	- each node has exactly one child and one parent 
	- following the path should produce no repeats
"""
def valid_path(path,expected_size=None):
	if expected_size is None: expected_size = path.size()
	seen = set([])
	current = path.current
	while True:
		if len(path.parents(current)) <= 1 \
			and len(path.children(current)) <= 1:
			if current not in seen:
				seen = seen | set([current])
				parents = path.parents(current)
				if len(parents) == 0:
					return True # The path is currently valid but incomplete
				current = parents [0]
				continue
			else:
				if len(seen) == expected_size:
					return True
				else:
					return False
		else:
			return False # There must only ever be a max of 1 parent and 1 child
		
	