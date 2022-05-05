#pragma once


namespace proxddp
{
  /// @brief  The Python bindings.
  namespace python {}
} // namespace proxddp

#include "proxddp/python/context.hpp"
#include "proxddp/python/macros.hpp"

#include <eigenpy/eigenpy.hpp>

namespace proxddp
{
  namespace python
  {
    namespace bp = boost::python;
    
    /// Expose ternary functions
    void exposeFunctions();
    void exposeCosts();
    void exposeNode();
    void exposeProblem();

    void exposeDynamics();
    void exposeIntegrators();
    void exposeSolvers();

  } // namespace python
} // namespace proxddp
