// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:action/Serve.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__ACTION__DETAIL__SERVE__BUILDER_HPP_
#define CUSTOM_MSGS__ACTION__DETAIL__SERVE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/action/detail/serve__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Serve_Goal_table_num
{
public:
  Init_Serve_Goal_table_num()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::action::Serve_Goal table_num(::custom_msgs::action::Serve_Goal::_table_num_type arg)
  {
    msg_.table_num = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Serve_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Serve_Goal>()
{
  return custom_msgs::action::builder::Init_Serve_Goal_table_num();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Serve_Result_move_result
{
public:
  Init_Serve_Result_move_result()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::action::Serve_Result move_result(::custom_msgs::action::Serve_Result::_move_result_type arg)
  {
    msg_.move_result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Serve_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Serve_Result>()
{
  return custom_msgs::action::builder::Init_Serve_Result_move_result();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Serve_Feedback_theta
{
public:
  explicit Init_Serve_Feedback_theta(::custom_msgs::action::Serve_Feedback & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Serve_Feedback theta(::custom_msgs::action::Serve_Feedback::_theta_type arg)
  {
    msg_.theta = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Serve_Feedback msg_;
};

class Init_Serve_Feedback_y
{
public:
  explicit Init_Serve_Feedback_y(::custom_msgs::action::Serve_Feedback & msg)
  : msg_(msg)
  {}
  Init_Serve_Feedback_theta y(::custom_msgs::action::Serve_Feedback::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Serve_Feedback_theta(msg_);
  }

private:
  ::custom_msgs::action::Serve_Feedback msg_;
};

class Init_Serve_Feedback_x
{
public:
  Init_Serve_Feedback_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_Feedback_y x(::custom_msgs::action::Serve_Feedback::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Serve_Feedback_y(msg_);
  }

private:
  ::custom_msgs::action::Serve_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Serve_Feedback>()
{
  return custom_msgs::action::builder::Init_Serve_Feedback_x();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Serve_SendGoal_Request_goal
{
public:
  explicit Init_Serve_SendGoal_Request_goal(::custom_msgs::action::Serve_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Serve_SendGoal_Request goal(::custom_msgs::action::Serve_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Serve_SendGoal_Request msg_;
};

class Init_Serve_SendGoal_Request_goal_id
{
public:
  Init_Serve_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_SendGoal_Request_goal goal_id(::custom_msgs::action::Serve_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Serve_SendGoal_Request_goal(msg_);
  }

private:
  ::custom_msgs::action::Serve_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Serve_SendGoal_Request>()
{
  return custom_msgs::action::builder::Init_Serve_SendGoal_Request_goal_id();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Serve_SendGoal_Response_stamp
{
public:
  explicit Init_Serve_SendGoal_Response_stamp(::custom_msgs::action::Serve_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Serve_SendGoal_Response stamp(::custom_msgs::action::Serve_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Serve_SendGoal_Response msg_;
};

class Init_Serve_SendGoal_Response_accepted
{
public:
  Init_Serve_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_SendGoal_Response_stamp accepted(::custom_msgs::action::Serve_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Serve_SendGoal_Response_stamp(msg_);
  }

private:
  ::custom_msgs::action::Serve_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Serve_SendGoal_Response>()
{
  return custom_msgs::action::builder::Init_Serve_SendGoal_Response_accepted();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Serve_GetResult_Request_goal_id
{
public:
  Init_Serve_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_msgs::action::Serve_GetResult_Request goal_id(::custom_msgs::action::Serve_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Serve_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Serve_GetResult_Request>()
{
  return custom_msgs::action::builder::Init_Serve_GetResult_Request_goal_id();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Serve_GetResult_Response_result
{
public:
  explicit Init_Serve_GetResult_Response_result(::custom_msgs::action::Serve_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Serve_GetResult_Response result(::custom_msgs::action::Serve_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Serve_GetResult_Response msg_;
};

class Init_Serve_GetResult_Response_status
{
public:
  Init_Serve_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_GetResult_Response_result status(::custom_msgs::action::Serve_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Serve_GetResult_Response_result(msg_);
  }

private:
  ::custom_msgs::action::Serve_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Serve_GetResult_Response>()
{
  return custom_msgs::action::builder::Init_Serve_GetResult_Response_status();
}

}  // namespace custom_msgs


namespace custom_msgs
{

namespace action
{

namespace builder
{

class Init_Serve_FeedbackMessage_feedback
{
public:
  explicit Init_Serve_FeedbackMessage_feedback(::custom_msgs::action::Serve_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::custom_msgs::action::Serve_FeedbackMessage feedback(::custom_msgs::action::Serve_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::action::Serve_FeedbackMessage msg_;
};

class Init_Serve_FeedbackMessage_goal_id
{
public:
  Init_Serve_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Serve_FeedbackMessage_feedback goal_id(::custom_msgs::action::Serve_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Serve_FeedbackMessage_feedback(msg_);
  }

private:
  ::custom_msgs::action::Serve_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::action::Serve_FeedbackMessage>()
{
  return custom_msgs::action::builder::Init_Serve_FeedbackMessage_goal_id();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__ACTION__DETAIL__SERVE__BUILDER_HPP_
