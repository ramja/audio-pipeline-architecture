WORKERS := 1

all:
	@echo "Durmiendo para que los servicios se alcancen a levantar"
	@echo "Zzzzzzz" && sleep 10
	@echo "Zzzzzzz" && sleep 10
	@echo "Despertando..."
	@python -m luigi --module etl AllTasks --workers $(WORKERS)

.PHONY: all
