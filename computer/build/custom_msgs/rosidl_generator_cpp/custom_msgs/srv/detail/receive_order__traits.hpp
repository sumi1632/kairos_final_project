// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msgs:srv/ReceiveOrder.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__TRAITS_HPP_
#define CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msgs/srv/detail/receive_order__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ReceiveOrder_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ReceiveOrder_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ReceiveOrder_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::srv::ReceiveOrder_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::srv::ReceiveOrder_Request & msg)
{
  return custom_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::srv::ReceiveOrder_Request>()
{
  return "custom_msgs::srv::ReceiveOrder_Request";
}

template<>
inline const char * name<custom_msgs::srv::ReceiveOrder_Request>()
{
  return "custom_msgs/srv/ReceiveOrder_Request";
}

template<>
struct has_fixed_size<custom_msgs::srv::ReceiveOrder_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_msgs::srv::ReceiveOrder_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_msgs::srv::ReceiveOrder_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'details'
#include "custom_msgs/msg/detail/order_detail__traits.hpp"

namespace custom_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const ReceiveOrder_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: details
  {
    if (msg.details.size() == 0) {
      out << "details: []";
    } else {
      out << "details: [";
      size_t pending_items = msg.details.size();
      for (auto item : msg.details) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ReceiveOrder_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: details
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.details.size() == 0) {
      out << "details: []\n";
    } else {
      out << "details:\n";
      for (auto item : msg.details) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ReceiveOrder_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::srv::ReceiveOrder_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::srv::ReceiveOrder_Response & msg)
{
  return custom_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::srv::ReceiveOrder_Response>()
{
  return "custom_msgs::srv::ReceiveOrder_Response";
}

template<>
inline const char * name<custom_msgs::srv::ReceiveOrder_Response>()
{
  return "custom_msgs/srv/ReceiveOrder_Response";
}

template<>
struct has_fixed_size<custom_msgs::srv::ReceiveOrder_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msgs::srv::ReceiveOrder_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msgs::srv::ReceiveOrder_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_msgs::srv::ReceiveOrder>()
{
  return "custom_msgs::srv::ReceiveOrder";
}

template<>
inline const char * name<custom_msgs::srv::ReceiveOrder>()
{
  return "custom_msgs/srv/ReceiveOrder";
}

template<>
struct has_fixed_size<custom_msgs::srv::ReceiveOrder>
  : std::integral_constant<
    bool,
    has_fixed_size<custom_msgs::srv::ReceiveOrder_Request>::value &&
    has_fixed_size<custom_msgs::srv::ReceiveOrder_Response>::value
  >
{
};

template<>
struct has_bounded_size<custom_msgs::srv::ReceiveOrder>
  : std::integral_constant<
    bool,
    has_bounded_size<custom_msgs::srv::ReceiveOrder_Request>::value &&
    has_bounded_size<custom_msgs::srv::ReceiveOrder_Response>::value
  >
{
};

template<>
struct is_service<custom_msgs::srv::ReceiveOrder>
  : std::true_type
{
};

template<>
struct is_service_request<custom_msgs::srv::ReceiveOrder_Request>
  : std::true_type
{
};

template<>
struct is_service_response<custom_msgs::srv::ReceiveOrder_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__TRAITS_HPP_
