#pragma once

#include <boost/python.hpp>

namespace proxddp {
namespace python {
namespace bp = boost::python;

template <typename T>
struct ClonePythonVisitor : bp::def_visitor<ClonePythonVisitor<T>> {
  template <typename PyT> void visit(PyT &obj) const {
    obj.def("clone", &T::clone, bp::args("self"), "Clone the object.");
  }
};

template <typename T>
struct CreateDataPythonVisitor : bp::def_visitor<CreateDataPythonVisitor<T>> {
  template <typename Pyclass> void visit(Pyclass &obj) const {
    obj.def("createData", &T::createData, bp::args("self"),
            "Create a data object.");
  }
};

template <typename T>
struct CopyableVisitor : bp::def_visitor<CopyableVisitor<T>> {
  template <typename PyClass> void visit(PyClass &obj) const {
    obj.def("copy", &copy, bp::arg("self"), "Returns a copy of this.");
  }

private:
  static T copy(const T &self) { return T(self); }
};

template <typename T>
struct PrintableVisitor : bp::def_visitor<PrintableVisitor<T>> {
  template <typename Pyclass> void visit(Pyclass &obj) const {
    obj.def(bp::self_ns::str(bp::self)).def(bp::self_ns::repr(bp::self));
  }
};

template <typename SolverType>
struct SolverVisitor : bp::def_visitor<SolverVisitor<SolverType>> {
  template <typename PyClass> void visit(PyClass &obj) const {
    obj.def_readwrite("verbose", &SolverType::verbose_,
                      "Verbosity level of the solver.")
        .def_readwrite("max_iters", &SolverType::max_iters,
                       "Maximum number of iterations.")
        .def_readwrite("ls_params", &SolverType::ls_params,
                       "Linesearch parameters.")
        .def_readwrite("target_tol", &SolverType::target_tol_,
                       "Target tolerance.")
        .def_readwrite("xreg", &SolverType::xreg_,
                       "Newton regularization parameter.")
        .def_readwrite("ureg", &SolverType::ureg_,
                       "Newton regularization parameter.")
        .def_readwrite("reg_init", &SolverType::reg_init)
        .def("getResults", &SolverType::getResults, bp::args("self"),
             bp::return_internal_reference<>(), "Get the results instance.")
        .def("getWorkspace", &SolverType::getWorkspace, bp::args("self"),
             bp::return_internal_reference<>(), "Get the workspace instance.")
        .def("setup", &SolverType::setup, bp::args("self", "problem"),
             "Allocate solver workspace and results data for the problem.")
        .def("registerCallback", &SolverType::registerCallback,
             bp::args("self", "cb"), "Add a callback to the solver.")
        .def("clearCallbacks", &SolverType::clearCallbacks, bp::args("self"),
             "Clear callbacks.");
  }
};

} // namespace python
} // namespace proxddp
