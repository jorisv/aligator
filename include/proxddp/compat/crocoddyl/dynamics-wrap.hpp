#pragma once

#include "proxddp/compat/crocoddyl/fwd.hpp"
#include "proxddp/core/explicit-dynamics.hpp"
#include <crocoddyl/core/action-base.hpp>

namespace proxddp {
namespace compat {
namespace croc {

template <typename Scalar>
struct DynamicsDataWrapperTpl : ExplicitDynamicsDataTpl<Scalar> {
  using Base = ExplicitDynamicsDataTpl<Scalar>;
  using CrocActionModel = crocoddyl::ActionModelAbstractTpl<Scalar>;
  explicit DynamicsDataWrapperTpl(const CrocActionModel *action_model)
      : Base(action_model->get_state()->get_ndx(), action_model->get_nu(),
             action_model->get_state()->get_nx(),
             action_model->get_state()->get_ndx()) {}
};

} // namespace croc
} // namespace compat
} // namespace proxddp