#include "proxddp/modelling/dynamics/integrator-euler.hpp"
#include "proxddp/modelling/dynamics/integrator-rk2.hpp"

#include <proxnlp/modelling/spaces/vector-space.hpp>

#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_SUITE(integrators)

BOOST_AUTO_TEST_CASE(euler) {
  using Manifold = proxnlp::VectorSpaceTpl<double>;
  constexpr int NX = 3;
  Manifold space(NX);
}

BOOST_AUTO_TEST_CASE(rk2) {
  using Manifold = proxnlp::VectorSpaceTpl<double>;
  constexpr int NX = 3;
  Manifold space(NX);
}

BOOST_AUTO_TEST_SUITE_END()