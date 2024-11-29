// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from my_custom_msgs:msg/UpdateStatus.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__TRAITS_HPP_
#define MY_CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "my_custom_msgs/msg/detail/update_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace my_custom_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const UpdateStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const UpdateStatus & msg,
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

  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const UpdateStatus & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace my_custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use my_custom_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const my_custom_msgs::msg::UpdateStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  my_custom_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use my_custom_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const my_custom_msgs::msg::UpdateStatus & msg)
{
  return my_custom_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<my_custom_msgs::msg::UpdateStatus>()
{
  return "my_custom_msgs::msg::UpdateStatus";
}

template<>
inline const char * name<my_custom_msgs::msg::UpdateStatus>()
{
  return "my_custom_msgs/msg/UpdateStatus";
}

template<>
struct has_fixed_size<my_custom_msgs::msg::UpdateStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<my_custom_msgs::msg::UpdateStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<my_custom_msgs::msg::UpdateStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MY_CUSTOM_MSGS__MSG__DETAIL__UPDATE_STATUS__TRAITS_HPP_
