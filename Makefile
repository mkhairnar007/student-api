.PHONY: install run clean

install:
	pip install -r requirements.txt

run: install
	python app.py

clean:
	rm -f students.db
