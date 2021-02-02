#include <Python.h>
#include "readkey.h"

PyObject *readkey(PyObject *self)
{
	return Py_BuildValue("i", _getch());
}
