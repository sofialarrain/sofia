class Person < ApplicationRecord
    has_many :vaccines, dependent: :destroy
    validates :name, presence: true
end
