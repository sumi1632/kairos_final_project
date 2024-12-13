// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msgs:msg/OrderDetail.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__TRAITS_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_msgs/msg/detail/order_detail__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const OrderDetail & msg,
  std::ostream & out)
{
  out << "{";
  // member: order_detail_id
  {
    out << "order_detail_id: ";
    rosidl_generator_traits::value_to_yaml(msg.order_detail_id, out);
    out << ", ";
  }

  // member: menu_name
  {
    out << "menu_name: ";
    rosidl_generator_traits::value_to_yaml(msg.menu_name, out);
    out << ", ";
  }

  // member: table_num
  {
    out << "table_num: ";
    rosidl_generator_traits::value_to_yaml(msg.table_num, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const OrderDetail & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: order_detail_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "order_detail_id: ";
    rosidl_generator_traits::value_to_yaml(msg.order_detail_id, out);
    out << "\n";
  }

  // member: menu_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "menu_name: ";
    rosidl_generator_traits::value_to_yaml(msg.menu_name, out);
    out << "\n";
  }

  // member: table_num
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "table_num: ";
    rosidl_generator_traits::value_to_yaml(msg.table_num, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const OrderDetail & msg, bool use_flow_style = false)
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

}  // namespace custom_msgs

namespace rosidl_generator_traits
{

[[deprecated("use custom_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_msgs::msg::OrderDetail & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_msgs::msg::OrderDetail & msg)
{
  return custom_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_msgs::msg::OrderDetail>()
{
  return "custom_msgs::msg::OrderDetail";
}

template<>
inline const char * name<custom_msgs::msg::OrderDetail>()
{
  return "custom_msgs/msg/OrderDetail";
}

template<>
struct has_fixed_size<custom_msgs::msg::OrderDetail>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<custom_msgs::msg::OrderDetail>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<custom_msgs::msg::OrderDetail>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSGS__MSG__DETAIL__ORDER_DETAIL__TRAITS_HPP_
