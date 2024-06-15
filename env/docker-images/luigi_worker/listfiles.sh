for f in /datalake/data/*.dat; do
    printf '%s,' "${f%.dat}"
done

