import React, { createContext, useContext, useState, type ReactNode } from "react";

interface User {
    id?: number
    email: string
    first_name?: string
    last_name: string
}

interface AuthContextType {
    user: User | null
    login: (userData: User) => void
    logout: () => void
    isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | null>(null)
    export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
        const [user, setUser] = useState<User | null>(null)

        const login = (userData: User) => {
            setUser(userData)
        }

        const logout = () => {
            setUser(null)
        }

        return (
            <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
                {children}
            </AuthContext.Provider>
        )
    }

export const useAuth = () => {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider')
    }
    return context
}