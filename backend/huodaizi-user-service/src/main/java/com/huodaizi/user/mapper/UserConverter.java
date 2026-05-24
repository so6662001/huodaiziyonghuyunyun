package com.huodaizi.user.mapper;

import com.huodaizi.user.dto.UserDTO;
import com.huodaizi.user.entity.User;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface UserConverter {

    UserDTO toDTO(User entity);
}
