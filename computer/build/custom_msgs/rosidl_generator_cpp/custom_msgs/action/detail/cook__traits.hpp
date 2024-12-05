// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msgs:action/Cook.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__ACTION__DETAIL__COOK__TRAITS_HPP_
#define CUSTOM_MSGS__ACTION__DETAIL__COOK__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msgs/action/detail/cook__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const Cook_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: menu_name
  {
    out << "menu_name: ";
    rosidl_generator_traits::value_to_yaml(msg.menu_name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Cook_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: menu_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "menu_name: ";
    rosidl_generator_traits::value_to_yaml(msg.menu_name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Cook_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::action::Cook_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::action::Cook_Goal & msg)
{
  return custom_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::action::Cook_Goal>()
{
  return "custom_msgs::action::Cook_Goal";
}

template<>
inline const char * name<custom_msgs::action::Cook_Goal>()
{
  return "custom_msgs/action/Cook_Goal";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msgs::action::Cook_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msgs::action::Cook_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace custom_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const Cook_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: cook_result
  {
    out << "cook_result: ";
    rosidl_generator_traits::value_to_yaml(msg.cook_result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Cook_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: cook_result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cook_result: ";
    rosidl_generator_traits::value_to_yaml(msg.cook_result, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Cook_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::action::Cook_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::action::Cook_Result & msg)
{
  return custom_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::action::Cook_Result>()
{
  return "custom_msgs::action::Cook_Result";
}

template<>
inline const char * name<custom_msgs::action::Cook_Result>()
{
  return "custom_msgs/action/Cook_Result";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msgs::action::Cook_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msgs::action::Cook_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace custom_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const Cook_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: cook_status
  {
    out << "cook_status: ";
    rosidl_generator_traits::value_to_yaml(msg.cook_status, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Cook_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: cook_status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cook_status: ";
    rosidl_generator_traits::value_to_yaml(msg.cook_status, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Cook_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::action::Cook_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::action::Cook_Feedback & msg)
{
  return custom_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::action::Cook_Feedback>()
{
  return "custom_msgs::action::Cook_Feedback";
}

template<>
inline const char * name<custom_msgs::action::Cook_Feedback>()
{
  return "custom_msgs/action/Cook_Feedback";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msgs::action::Cook_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msgs::action::Cook_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "custom_msgs/action/detail/cook__traits.hpp"

namespace custom_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const Cook_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Cook_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Cook_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::action::Cook_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::action::Cook_SendGoal_Request & msg)
{
  return custom_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::action::Cook_SendGoal_Request>()
{
  return "custom_msgs::action::Cook_SendGoal_Request";
}

template<>
inline const char * name<custom_msgs::action::Cook_SendGoal_Request>()
{
  return "custom_msgs/action/Cook_SendGoal_Request";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<custom_msgs::action::Cook_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<custom_msgs::action::Cook_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<custom_msgs::action::Cook_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<custom_msgs::action::Cook_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace custom_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const Cook_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Cook_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Cook_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::action::Cook_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::action::Cook_SendGoal_Response & msg)
{
  return custom_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::action::Cook_SendGoal_Response>()
{
  return "custom_msgs::action::Cook_SendGoal_Response";
}

template<>
inline const char * name<custom_msgs::action::Cook_SendGoal_Response>()
{
  return "custom_msgs/action/Cook_SendGoal_Response";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<custom_msgs::action::Cook_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<custom_msgs::action::Cook_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_msgs::action::Cook_SendGoal>()
{
  return "custom_msgs::action::Cook_SendGoal";
}

template<>
inline const char * name<custom_msgs::action::Cook_SendGoal>()
{
  return "custom_msgs/action/Cook_SendGoal";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_msgs::action::Cook_SendGoal_Request>::value &&
    has_fixed_size<custom_msgs::action::Cook_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_msgs::action::Cook_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_msgs::action::Cook_SendGoal_Request>::value &&
    has_bounded_size<custom_msgs::action::Cook_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<custom_msgs::action::Cook_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<custom_msgs::action::Cook_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_msgs::action::Cook_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace custom_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const Cook_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Cook_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Cook_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::action::Cook_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::action::Cook_GetResult_Request & msg)
{
  return custom_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::action::Cook_GetResult_Request>()
{
  return "custom_msgs::action::Cook_GetResult_Request";
}

template<>
inline const char * name<custom_msgs::action::Cook_GetResult_Request>()
{
  return "custom_msgs/action/Cook_GetResult_Request";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<custom_msgs::action::Cook_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<custom_msgs::action::Cook_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "custom_msgs/action/detail/cook__traits.hpp"

namespace custom_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const Cook_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Cook_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Cook_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::action::Cook_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::action::Cook_GetResult_Response & msg)
{
  return custom_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::action::Cook_GetResult_Response>()
{
  return "custom_msgs::action::Cook_GetResult_Response";
}

template<>
inline const char * name<custom_msgs::action::Cook_GetResult_Response>()
{
  return "custom_msgs/action/Cook_GetResult_Response";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<custom_msgs::action::Cook_Result>::value> {};

template<>
struct has_bounded_size<custom_msgs::action::Cook_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<custom_msgs::action::Cook_Result>::value> {};

template<>
struct is_message<custom_msgs::action::Cook_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_msgs::action::Cook_GetResult>()
{
  return "custom_msgs::action::Cook_GetResult";
}

template<>
inline const char * name<custom_msgs::action::Cook_GetResult>()
{
  return "custom_msgs/action/Cook_GetResult";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_msgs::action::Cook_GetResult_Request>::value &&
    has_fixed_size<custom_msgs::action::Cook_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_msgs::action::Cook_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_msgs::action::Cook_GetResult_Request>::value &&
    has_bounded_size<custom_msgs::action::Cook_GetResult_Response>::value
  >
{
};

template<>
struct is_service<custom_msgs::action::Cook_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<custom_msgs::action::Cook_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_msgs::action::Cook_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "custom_msgs/action/detail/cook__traits.hpp"

namespace custom_msgs
{

namespace action
{

inline void to_flow_style_yaml(
  const Cook_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Cook_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Cook_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::action::Cook_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::action::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::action::Cook_FeedbackMessage & msg)
{
  return custom_msgs::action::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::action::Cook_FeedbackMessage>()
{
  return "custom_msgs::action::Cook_FeedbackMessage";
}

template<>
inline const char * name<custom_msgs::action::Cook_FeedbackMessage>()
{
  return "custom_msgs/action/Cook_FeedbackMessage";
}

template<>
struct has_fixed_size<custom_msgs::action::Cook_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<custom_msgs::action::Cook_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<custom_msgs::action::Cook_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<custom_msgs::action::Cook_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<custom_msgs::action::Cook_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<custom_msgs::action::Cook>
  : std::true_type
{
};

template<>
struct is_action_goal<custom_msgs::action::Cook_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<custom_msgs::action::Cook_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<custom_msgs::action::Cook_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // CUSTOM_MSGS__ACTION__DETAIL__COOK__TRAITS_HPP_
