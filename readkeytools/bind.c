#include "readkey.h"

PyMethodDef methods[] = {
	{"readkey", (PyCFunction)readkey, METH_NOARGS, "read key using getch"},
	{NULL}};

PyModuleDef readkeytools_module = {
	PyModuleDef_HEAD_INIT,
	"readkeytools",
	NULL,
	-1,
	methods};

PyMODINIT_FUNC PyInit_readkeytools(void)
{
	return PyModule_Create(&readkeytools_module);
}
