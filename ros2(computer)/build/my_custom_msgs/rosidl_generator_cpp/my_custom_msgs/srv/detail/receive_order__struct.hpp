// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_custom_msgs:srv/ReceiveOrder.idl
// generated code does not contain a copyright notice

#ifndef MY_CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_HPP_
#define MY_CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_custom_msgs__srv__ReceiveOrder_Request __attribute__((deprecated))
#else
# define DEPRECATED__my_custom_msgs__srv__ReceiveOrder_Request __declspec(deprecated)
#endif

namespace my_custom_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ReceiveOrder_Request_
{
  using Type = ReceiveOrder_Request_<ContainerAllocator>;

  explicit ReceiveOrder_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ul;
    }
  }

  explicit ReceiveOrder_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ul;
    }
  }

  // field types and members
  using _id_type =
    uint32_t;
  _id_type id;

  // setters for named parameter idiom
  Type & set__id(
    const uint32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_custom_msgs__srv__ReceiveOrder_Request
    std::shared_ptr<my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_custom_msgs__srv__ReceiveOrder_Request
    std::shared_ptr<my_custom_msgs::srv::ReceiveOrder_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ReceiveOrder_Request_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ReceiveOrder_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ReceiveOrder_Request_

// alias to use template instance with default allocator
using ReceiveOrder_Request =
  my_custom_msgs::srv::ReceiveOrder_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace my_custom_msgs


// Include directives for member types
// Member 'details'
#include "my_custom_msgs/msg/detail/order_detail__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__my_custom_msgs__srv__ReceiveOrder_Response __attribute__((deprecated))
#else
# define DEPRECATED__my_custom_msgs__srv__ReceiveOrder_Response __declspec(deprecated)
#endif

namespace my_custom_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ReceiveOrder_Response_
{
  using Type = ReceiveOrder_Response_<ContainerAllocator>;

  explicit ReceiveOrder_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit ReceiveOrder_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _details_type =
    std::vector<my_custom_msgs::msg::OrderDetail_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<my_custom_msgs::msg::OrderDetail_<ContainerAllocator>>>;
  _details_type details;

  // setters for named parameter idiom
  Type & set__details(
    const std::vector<my_custom_msgs::msg::OrderDetail_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<my_custom_msgs::msg::OrderDetail_<ContainerAllocator>>> & _arg)
  {
    this->details = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_custom_msgs__srv__ReceiveOrder_Response
    std::shared_ptr<my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_custom_msgs__srv__ReceiveOrder_Response
    std::shared_ptr<my_custom_msgs::srv::ReceiveOrder_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ReceiveOrder_Response_ & other) const
  {
    if (this->details != other.details) {
      return false;
    }
    return true;
  }
  bool operator!=(const ReceiveOrder_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ReceiveOrder_Response_

// alias to use template instance with default allocator
using ReceiveOrder_Response =
  my_custom_msgs::srv::ReceiveOrder_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace my_custom_msgs

namespace my_custom_msgs
{

namespace srv
{

struct ReceiveOrder
{
  using Request = my_custom_msgs::srv::ReceiveOrder_Request;
  using Response = my_custom_msgs::srv::ReceiveOrder_Response;
};

}  // namespace srv

}  // namespace my_custom_msgs

#endif  // MY_CUSTOM_MSGS__SRV__DETAIL__RECEIVE_ORDER__STRUCT_HPP_
