clean-reqs:
    rm requirements.txt test-requirements.txt

make-reqs:
    pip-compile --strip-extras --no-annotate --no-header requirements.in
    pip-compile --strip-extras --no-annotate --no-header test-requirements.in

run-litestar:
    uvicorn fastapi_vs_litestar.svc_litestar.app:app --port 5005 --reload

test-litestar:
    python fastapi_vs_litestar/svc_litestar/tests/test_app.py

stress-litestar:
    echo TODO

run-fastapi:
    uvicorn fastapi_vs_litestar.svc_fastapi.app:app --port 5006 --reload

test-fastapi:
    python fastapi_vs_litestar/svc_fastapi/tests/test_app.py

stress-fastapi:
    echo TODO