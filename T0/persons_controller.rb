class PersonsController < ApplicationController
    def index
        @all_persons = Person.all
        render json: @all_persons
    end

    def create
        @person = Person.new(person_params)
        @person.save
        if @person.save
            render json: @person
        else
            render json: @person.errors, status: :unprocessable_entity
        end
    end
    
    def person_params
        params.require(:person).permit(:name)
    end

    def show
        if params.key?(:id)
            @person = Person.find(params[:id])
            render json: @person
        else
            @persons = Person.all_persons
            render json: @persons
        end
    end

    def destroy_all
        Person.all.destroy_all
    end
end
