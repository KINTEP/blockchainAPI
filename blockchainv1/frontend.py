
@app.route('/')
def home():
	return render_template('home.html')

@app.route('/chain')
def chain():
	return blockchain.main_chain()

@app.route('/mine')
def mine():
	return render_template('index2.html')

@app.route('/add_block')
def add_block():
	return "<h1>Hello KUMI ISAAC NEWTON</h1>"

@app.route('/create_transaction')
def create_transaction():
	pass
