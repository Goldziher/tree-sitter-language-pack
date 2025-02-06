#include <Python.h>

typedef struct TSLanguage TSLanguage;

#ifndef TS_LANGUAGE_NAME
#error TS_LANGUAGE_NAME must be defined
#endif

#define _str(s) #s
#define str(s) _str(s)
#define _cat(a, b) a##b
#define cat(a, b) _cat(a, b)

#define TS_LANGUAGE_FUNC cat(tree_sitter_, TS_LANGUAGE_NAME) // Expands to tree_sitter_<language_name>
#define TS_LANGUAGE_METHOD cat(TS_LANGUAGE_NAME, _language) // Expands to <language_name>_language
#define TS_LANGUAGE_MODULE cat(PyInit_, TS_LANGUAGE_NAME) // Expands to PyInit_<language_name>

TSLanguage *TS_LANGUAGE_FUNC(void); // Expands to tree_sitter_<language_name>(void), e.g. tree_sitter_python(void)

// Python method that wraps the TS_LANGUAGE_FUNC and returns a pointer to the TSLanguage struct
static PyObject* TS_LANGUAGE_METHOD(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(args)) {
    return PyCapsule_New(TS_LANGUAGE_FUNC(), "tree_sitter.Language", NULL);
}

// Method definition table for the module
static PyMethodDef methods[] = {
    {"language", TS_LANGUAGE_METHOD, METH_NOARGS, "Get the tree-sitter language for this grammar."},
    {NULL, NULL, 0, NULL}
};

// Module definition structure
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    .m_name = str(TS_LANGUAGE_NAME), // Expands to the language name as a string
    .m_doc = NULL,
    .m_size = -1,
    .m_methods = methods
};

// Module initialization function
PyMODINIT_FUNC TS_LANGUAGE_MODULE(void) {
    return PyModule_Create(&module);
}
